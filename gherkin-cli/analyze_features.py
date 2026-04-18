#!/usr/bin/env python3
"""
CukeLinter Analysis Script
Performs static analysis on feature files using cuke_linter
"""

import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any


class FeatureLinter:
    """Run cuke_linter analysis on feature files."""
    
    def __init__(self, features_dir: str = "features"):
        self.features_dir = features_dir
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)
    
    def run_linter(self, output_format: str = "json") -> Dict[str, Any]:
        """Run cuke_linter and capture output."""
        try:
            cmd = [
                "cuke_linter",
                "--out", output_format,
                self.features_dir
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            
            return {
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0
            }
        except FileNotFoundError:
            return {
                "error": "cuke_linter not found. Install with: pip install cuke-linter",
                "success": False
            }
    
    def run_pretty_analysis(self) -> str:
        """Run linter with pretty output."""
        try:
            cmd = ["cuke_linter", self.features_dir]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            return result.stdout
        except FileNotFoundError:
            return "cuke_linter not installed"
    
    def save_report(self, output: str, filename: str):
        """Save linter output to file."""
        report_path = self.reports_dir / filename
        with open(report_path, 'w') as f:
            f.write(output)
        return report_path
    
    def analyze(self) -> Dict[str, Any]:
        """Run complete analysis."""
        print("\n" + "=" * 60)
        print("🔍 Running CukeLinter Static Analysis")
        print("=" * 60 + "\n")
        
        # Run pretty output
        pretty_output = self.run_pretty_analysis()
        
        if pretty_output.startswith("cuke_linter"):
            print(pretty_output)
            return {"error": "cuke_linter not installed"}
        
        # Save reports
        print("📊 Analyzing feature files...")
        
        # Save pretty report
        report_path = self.save_report(pretty_output, "linter_report.txt")
        print(f"✅ Report saved: {report_path}")
        
        # Display output
        print("\n" + pretty_output)
        
        # Parse results for summary
        lines = pretty_output.split('\n')
        issues = [l for l in lines if l.strip() and not l.startswith('Linting')]
        issue_count = len([l for l in issues if l.strip()])
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "features_dir": self.features_dir,
            "issues_found": issue_count,
            "report_file": str(report_path)
        }
        
        # Save summary as JSON
        summary_path = self.reports_dir / "linter_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print("\n" + "=" * 60)
        print("📁 Reports Generated:")
        print("=" * 60)
        print(f"  📄 {report_path.name}")
        print(f"  📊 {summary_path.name}")
        print("\n")
        
        return summary


def main():
    """Run feature file analysis."""
    import sys
    
    features_dir = sys.argv[1] if len(sys.argv) > 1 else "features"
    
    linter = FeatureLinter(features_dir)
    linter.analyze()


if __name__ == "__main__":
    main()
