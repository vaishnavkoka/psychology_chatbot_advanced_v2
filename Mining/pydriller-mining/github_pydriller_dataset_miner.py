"""
Robust GitHub + PyDriller miner for Gherkin dataset creation.

What it does:
- Discovers repositories by searching for real .feature files on GitHub
- Mines commit history of discovered repositories using PyDriller
- Extracts scenarios and steps from feature files
- Builds a deduplicated scenario-level dataset
- Creates train/val/test split by repository to reduce leakage

Usage example:
    export GITHUB_TOKEN=your_new_token
    python3 github_pydriller_dataset_miner.py --max-repos 40 --min-stars 30
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
import requests
from pydriller import Repository


GITHUB_API = "https://api.github.com"
FEATURE_EXT = ".feature"


@dataclass
class RepoCandidate:
    full_name: str
    html_url: str
    clone_url: str
    default_branch: str
    stars: int
    language: Optional[str]


class GitHubClient:
    def __init__(self, token_env: str = "GITHUB_TOKEN", timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        token = os.getenv(token_env, "").strip()
        self.has_token = False
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
            self.has_token = True
        else:
            print(
                "⚠️  WARNING: GitHub token not found in environment variable '{token_env}'.\n"
                "   Without a token, you are limited to 60 API requests/hour.\n"
                "   With a token, you get 5000 requests/hour.\n"
                "   To set a token, run: export GITHUB_TOKEN=your_token\n"
            )

    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        retries = 5
        backoff = 1.5

        for attempt in range(1, retries + 1):
            resp = self.session.request(
                method,
                url,
                headers=self.headers,
                timeout=self.timeout,
                **kwargs,
            )

            if resp.status_code in (429, 502, 503, 504):
                time.sleep(backoff)
                backoff *= 2
                continue

            if resp.status_code == 403 and "X-RateLimit-Remaining" in resp.headers:
                remaining = resp.headers.get("X-RateLimit-Remaining", "1")
                reset_at = int(resp.headers.get("X-RateLimit-Reset", "0") or "0")
                if remaining == "0" and reset_at > 0:
                    sleep_for = max(1, reset_at - int(time.time()) + 1)
                    print(f"Rate limit reached, sleeping for {sleep_for}s...")
                    time.sleep(min(sleep_for, 120))
                    continue

            return resp

        return resp

    def validate_token(self) -> bool:
        """Check if token is valid and we have API access."""
        if not self.has_token:
            return False

        resp = self._request(
            "GET",
            f"{GITHUB_API}/user",
        )
        if resp.status_code == 200:
            data = resp.json()
            print(f"✓ Token validated for user: {data.get('login')}")
            return True
        else:
            print(f"✗ Token validation failed: {resp.status_code} {resp.text[:200]}")
            return False

    def search_feature_repositories(
        self,
        max_repos: int,
        min_stars: int,
        per_page: int = 100,
    ) -> List[RepoCandidate]:
        """Discover repositories containing feature files via code search."""

        repos: Dict[str, RepoCandidate] = {}
        page = 1

        # Language-agnostic discovery: require .feature files and minimum stars.
        query = f"filename:.feature stars:>={min_stars}"

        while len(repos) < max_repos and page <= 10:
            resp = self._request(
                "GET",
                f"{GITHUB_API}/search/code",
                params={
                    "q": query,
                    "sort": "indexed",
                    "order": "desc",
                    "per_page": per_page,
                    "page": page,
                },
            )

            if resp.status_code != 200:
                print(f"GitHub search/code failed: {resp.status_code} {resp.text[:300]}")
                break

            data = resp.json()
            items = data.get("items", [])
            if not items:
                break

            for item in items:
                repo = item.get("repository", {})
                full_name = repo.get("full_name")
                if not full_name or full_name in repos:
                    continue

                repos[full_name] = RepoCandidate(
                    full_name=full_name,
                    html_url=repo.get("html_url", ""),
                    clone_url=repo.get("clone_url", ""),
                    default_branch=repo.get("default_branch", "main"),
                    stars=repo.get("stargazers_count", 0),
                    language=repo.get("language"),
                )

                if len(repos) >= max_repos:
                    break

            print(f"Discovery page {page}: {len(repos)} repositories collected")
            page += 1

        return list(repos.values())

    def get_feature_file_count(self, repo_full_name: str) -> int:
        """Return confirmed .feature file count in a repository via GitHub code search."""
        resp = self._request(
            "GET",
            f"{GITHUB_API}/search/code",
            params={
                "q": f"repo:{repo_full_name} filename:.feature",
                "per_page": 1,
                "page": 1,
            },
        )

        if resp.status_code != 200:
            return 0

        data = resp.json()
        return int(data.get("total_count", 0) or 0)


def normalize_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def normalize_scenario_name(text: str) -> str:
    text = normalize_ws(text).lower()
    text = re.sub(r"[^a-z0-9 ]+", "", text)
    return text


def stable_split(repo_full_name: str) -> str:
    """Stable split by repository hash to avoid train/test leakage."""
    h = int(hashlib.sha1(repo_full_name.encode("utf-8")).hexdigest(), 16) % 100
    if h < 80:
        return "train"
    if h < 90:
        return "val"
    return "test"


def parse_iso_date(date_text: Optional[str]) -> Optional[datetime]:
    """Parse YYYY-MM-DD or ISO datetime text into datetime."""
    if not date_text:
        return None

    value = date_text.strip()
    if not value:
        return None

    try:
        if len(value) == 10:
            return datetime.strptime(value, "%Y-%m-%d")
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(
            f"Invalid date '{date_text}'. Use YYYY-MM-DD or ISO datetime format."
        ) from exc


def count_step_lines(steps: str) -> int:
    if not steps:
        return 0
    return sum(
        1
        for line in steps.splitlines()
        if re.match(r"^(Given|When|Then|And|But)\b", line.strip(), flags=re.IGNORECASE)
    )


def looks_like_low_quality_name(name: str) -> bool:
    norm = normalize_ws(name)
    if len(norm) < 8:
        return True

    low_value_patterns = [
        r"^test\b",
        r"^scenario\s*\d+$",
        r"^example\s*\d*$",
        r"^todo\b",
        r"^wip\b",
        r"^sample\b",
    ]
    return any(re.search(pat, norm, flags=re.IGNORECASE) for pat in low_value_patterns)


def parse_feature_scenarios(feature_text: str) -> List[Dict[str, str]]:
    """Extract scenario blocks with steps from a feature file body."""
    lines = (feature_text or "").splitlines()

    results: List[Dict[str, str]] = []
    current_name = ""
    current_type = ""
    current_steps: List[str] = []

    def flush_current() -> None:
        nonlocal current_name, current_type, current_steps
        if current_name:
            results.append(
                {
                    "scenario_name": normalize_ws(current_name),
                    "scenario_type": current_type,
                    "steps": "\n".join(current_steps).strip(),
                }
            )
        current_name = ""
        current_type = ""
        current_steps = []

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            if current_name and current_steps:
                current_steps.append("")
            continue

        if stripped.lower().startswith("scenario outline:"):
            flush_current()
            current_type = "scenario_outline"
            current_name = stripped.split(":", 1)[1].strip()
            continue

        if stripped.lower().startswith("scenario:"):
            flush_current()
            current_type = "scenario"
            current_name = stripped.split(":", 1)[1].strip()
            continue

        if current_name and re.match(r"^(Given|When|Then|And|But)\b", stripped, flags=re.IGNORECASE):
            current_steps.append(stripped)
            continue

        if current_name and stripped.lower().startswith("examples:"):
            current_steps.append(stripped)
            continue

        if current_name and stripped.startswith("|"):
            current_steps.append(stripped)

    flush_current()
    return results


class DatasetMiner:
    def __init__(
        self,
        output_dir: Path,
        max_repos: int,
        min_stars: int,
        min_feature_files: int,
        token_env: str,
        workers: int,
        since: Optional[datetime],
        until: Optional[datetime],
        min_steps: int,
        max_steps: int,
        keep_outlines_only: bool,
        skip_verification: bool = False,
    ):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.max_repos = max_repos
        self.min_stars = min_stars
        self.min_feature_files = max(1, min_feature_files)
        self.skip_verification = skip_verification
        self.workers = max(1, workers)
        self.since = since
        self.until = until
        self.min_steps = max(1, min_steps)
        self.max_steps = max(self.min_steps, max_steps)
        self.keep_outlines_only = keep_outlines_only
        self.github = GitHubClient(token_env=token_env)
        self.started_at = datetime.now(timezone.utc).isoformat()

    def discover_repositories(self) -> List[RepoCandidate]:
        discovered = self.github.search_feature_repositories(
            max_repos=self.max_repos,
            min_stars=self.min_stars,
        )
        print(f"Total discovered repositories (pre-verify): {len(discovered)}")

        if self.skip_verification:
            print("Skipping .feature file count verification (--skip-verification=true)")
            return discovered

        verified: List[RepoCandidate] = []
        for repo in discovered:
            feature_count = self.github.get_feature_file_count(repo.full_name)
            if feature_count >= self.min_feature_files:
                verified.append(repo)
                print(
                    f"Verified {repo.full_name}: {feature_count} .feature files"
                )
            else:
                print(
                    f"Skipped {repo.full_name}: {feature_count} .feature files (min required: {self.min_feature_files})"
                )

        print(f"Total verified repositories: {len(verified)}")
        return verified

    def mine_repository(self, repo: RepoCandidate) -> List[Dict[str, object]]:
        print(f"Mining {repo.full_name} ...")

        scenario_stats: Dict[Tuple[str, str], Dict[str, object]] = {}

        try:
            walker = Repository(
                repo.clone_url,
                only_in_branch=repo.default_branch,
                only_modifications_with_file_types=[FEATURE_EXT],
                since=self.since,
                to=self.until,
            )

            commit_count = 0
            for commit in walker.traverse_commits():
                commit_count += 1
                for mf in commit.modified_files:
                    if not mf.filename.endswith(FEATURE_EXT):
                        continue

                    if not mf.source_code:
                        continue

                    feature_path = mf.new_path or mf.old_path or mf.filename
                    scenarios = parse_feature_scenarios(mf.source_code)
                    for scenario in scenarios:
                        key = (feature_path, normalize_scenario_name(scenario["scenario_name"]))
                        rec = scenario_stats.get(key)
                        if rec is None:
                            rec = {
                                "repo_full_name": repo.full_name,
                                "repo_url": repo.html_url,
                                "repo_clone_url": repo.clone_url,
                                "default_branch": repo.default_branch,
                                "repo_stars": repo.stars,
                                "repo_language": repo.language,
                                "feature_path": feature_path,
                                "scenario_name": scenario["scenario_name"],
                                "scenario_type": scenario["scenario_type"],
                                "steps": scenario["steps"],
                                "first_seen": commit.committer_date.isoformat(),
                                "last_seen": commit.committer_date.isoformat(),
                                "commits_touched": 1,
                                "authors": {commit.author.name},
                                "latest_commit": commit.hash,
                                "latest_message": normalize_ws(commit.msg.split("\n", 1)[0]),
                            }
                            scenario_stats[key] = rec
                        else:
                            rec["last_seen"] = commit.committer_date.isoformat()
                            rec["commits_touched"] = int(rec["commits_touched"]) + 1
                            rec["authors"].add(commit.author.name)
                            rec["latest_commit"] = commit.hash
                            rec["latest_message"] = normalize_ws(commit.msg.split("\n", 1)[0])

            records = []
            for value in scenario_stats.values():
                value["authors_count"] = len(value["authors"])
                value["authors"] = "; ".join(sorted(value["authors"]))
                value["split"] = stable_split(value["repo_full_name"])
                value["steps_count"] = count_step_lines(value["steps"])
                value["scenario_fingerprint"] = hashlib.sha1(
                    (value["repo_full_name"] + "|" + value["feature_path"] + "|" + value["scenario_name"] + "|" + value["steps"]).encode("utf-8")
                ).hexdigest()
                records.append(value)

            print(
                f"  commits scanned: {commit_count}, unique scenarios: {len(records)}"
            )
            return records

        except Exception as exc:
            print(f"  mining failed for {repo.full_name}: {exc}")
            return []

    def _mine_repositories_parallel(self, repos: List[RepoCandidate]) -> List[Dict[str, object]]:
        """Mine repositories concurrently for faster throughput."""
        all_rows: List[Dict[str, object]] = []
        total = len(repos)

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            future_map = {
                executor.submit(self.mine_repository, repo): repo.full_name for repo in repos
            }

            done = 0
            for future in as_completed(future_map):
                done += 1
                repo_name = future_map[future]
                try:
                    rows = future.result()
                    all_rows.extend(rows)
                    print(f"Progress: {done}/{total} repos finished ({repo_name})")
                except Exception as exc:
                    print(f"Progress: {done}/{total} repos finished ({repo_name}) failed: {exc}")

        return all_rows

    def _quality_filter(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, int]]:
        """Apply quality filters so the dataset is cleaner for LLM training."""
        stats: Dict[str, int] = {"before_quality_filter": int(len(df))}

        # Enforce step count quality boundaries.
        df = df[df["steps_count"].between(self.min_steps, self.max_steps)]
        stats["after_steps_filter"] = int(len(df))

        # Remove low-information scenario names.
        df = df[~df["scenario_name"].apply(looks_like_low_quality_name)]
        stats["after_name_filter"] = int(len(df))

        # Optional mode useful for richer data generation patterns.
        if self.keep_outlines_only:
            df = df[df["scenario_type"] == "scenario_outline"]
        stats["after_outline_filter"] = int(len(df))

        # Remove exact duplicates after filters.
        df = df.drop_duplicates(subset=["scenario_fingerprint"]).reset_index(drop=True)
        stats["after_final_dedup"] = int(len(df))

        return df, stats

    def run(self, output_prefix: str) -> Dict[str, object]:
        repos = self.discover_repositories()
        all_rows = self._mine_repositories_parallel(repos)

        if not all_rows:
            raise RuntimeError("No rows were mined. Try lowering min_stars or increasing max_repos.")

        df = pd.DataFrame(all_rows)

        before = len(df)
        df, quality_stats = self._quality_filter(df)
        after = len(df)

        dataset_path = self.output_dir / f"{output_prefix}_scenario_dataset.csv"
        df.to_csv(dataset_path, index=False)

        jsonl_path = self.output_dir / f"{output_prefix}_scenario_dataset.jsonl"
        with open(jsonl_path, "w", encoding="utf-8") as f:
            for row in df.to_dict(orient="records"):
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

        split_stats = df.groupby("split")["scenario_fingerprint"].count().to_dict()

        summary = {
            "started_at": self.started_at,
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "discovered_repositories": len(repos),
            "workers": self.workers,
            "skip_verification": self.skip_verification,
            "since": self.since.isoformat() if self.since else None,
            "until": self.until.isoformat() if self.until else None,
            "min_steps": self.min_steps,
            "max_steps": self.max_steps,
            "min_feature_files": self.min_feature_files,
            "keep_outlines_only": self.keep_outlines_only,
            "rows_before_dedup": before,
            "rows_after_dedup": after,
            "quality_filter_stats": quality_stats,
            "split_stats": split_stats,
            "dataset_csv": str(dataset_path),
            "dataset_jsonl": str(jsonl_path),
        }

        summary_path = self.output_dir / f"{output_prefix}_summary.json"
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        print("\nMining complete")
        print(f"CSV: {dataset_path}")
        print(f"JSONL: {jsonl_path}")
        print(f"Summary: {summary_path}")
        print(f"Split counts: {split_stats}")

        return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Mine Gherkin scenario dataset from GitHub with PyDriller")
    parser.add_argument("--max-repos", type=int, default=30, help="Maximum repositories to mine")
    parser.add_argument("--min-stars", type=int, default=30, help="Minimum stars for repository discovery")
    parser.add_argument(
        "--min-feature-files",
        type=int,
        default=1,
        help="Minimum confirmed .feature files required per repository",
    )
    parser.add_argument("--workers", type=int, default=4, help="Parallel repository mining workers")
    parser.add_argument("--since", type=str, default="", help="Mine commits since date (YYYY-MM-DD or ISO datetime)")
    parser.add_argument("--until", type=str, default="", help="Mine commits until date (YYYY-MM-DD or ISO datetime)")
    parser.add_argument("--min-steps", type=int, default=3, help="Minimum Given/When/Then steps per scenario")
    parser.add_argument("--max-steps", type=int, default=30, help="Maximum Given/When/Then steps per scenario")
    parser.add_argument(
        "--keep-outlines-only",
        action="store_true",
        help="Keep only Scenario Outline samples",
    )
    parser.add_argument(
        "--skip-verification",
        type=lambda x: x.lower() == "true",
        default=False,
        help="Skip .feature file count verification per repo to save API calls",
    )
    parser.add_argument(
        "--token-env",
        type=str,
        default="GITHUB_TOKEN",
        help="Environment variable that stores GitHub token",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(Path(__file__).parent / "mining_outputs"),
        help="Directory where datasets are saved",
    )
    parser.add_argument("--output-prefix", type=str, default="best_miner", help="Output file prefix")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    since = parse_iso_date(args.since)
    until = parse_iso_date(args.until)
    print("\n" + "="*80)
    print("GHERKIN DATASET MINER (GitHub + PyDriller)")
    print("="*80 + "\n")

    github_client = GitHubClient(token_env=args.token_env)
    if not github_client.has_token:
        print(
            "⚠️  No token detected. Mining will be slow due to GitHub API rate limits.\n"
            "    Set token now: export GITHUB_TOKEN=your_token\n"
        )
    else:
        print("Validating GitHub token...")
        if not github_client.validate_token():
            print("\n❌ Token validation failed. Check your GITHUB_TOKEN environment variable.\n")
            return

    miner = DatasetMiner(
        output_dir=Path(args.output_dir),
        max_repos=args.max_repos,
        min_stars=args.min_stars,
        min_feature_files=args.min_feature_files,
        token_env=args.token_env,
        workers=args.workers,
        since=since,
        until=until,
        min_steps=args.min_steps,
        max_steps=args.max_steps,
        keep_outlines_only=args.keep_outlines_only,
        skip_verification=args.skip_verification,
    )
    miner.run(output_prefix=args.output_prefix)


if __name__ == "__main__":
    main()
