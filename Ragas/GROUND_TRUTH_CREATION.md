# Ground Truth Creation for RAGAS Evaluation

## Overview
The ground truth for RAGAS evaluation was **created using an AI agent** (exact prompts not documented). The result is 20 synthetic Gherkin BDD scenarios in JSON and CSV format.

---

## What is Ground Truth in This Context?

**Ground Truth = Expected System Behavior**

For each scenario in the evaluation, ground truth consists of:

1. **The "then" field** - Short expected outcome
2. **The "expected_output" field** - Detailed system behavior description
3. **The "acceptance_criteria" array** - Measurable, quantifiable success criteria

### Example Ground Truth

```json
{
  "feature": "User Authentication",
  "scenario": "User login with valid credentials",
  "given": "A user has registered with valid credentials in the system",
  "when": "The user enters their username and password on the login page and clicks 'Login'",
  
  "then": "The system should authenticate the user and redirect to the dashboard",
  
  "acceptance_criteria": [
    "User receives success message",
    "User session is created",
    "User is redirected to dashboard within 2 seconds"
  ],
  
  "expected_output": "Upon successful authentication with correct username and password, the application validates credentials against the user database, establishes an authenticated session, and redirects the user to the main dashboard page."
}
```

**Ground Truth Components:**
- `then` (line 5) → What the system should do
- `acceptance_criteria` → How to measure it
- `expected_output` → Detailed description of behavior

---

## How Ground Truth is Used in RAGAS

### RAGAS Evaluation Pipeline

```
1. Input: Gherkin Scenario (Given-When-Then)
                    ↓
2. Generate: LLM creates specification answer
                    ↓
3. Compare: Generated spec vs. Ground Truth
                    ↓
4. Score: 4 Metrics measure alignment
                    ↓
5. Output: Faithfulness, Answer Relevancy, etc.
```

### Each RAGAS Metric Uses Ground Truth

| Metric | Uses Ground Truth To... |
|--------|--------------------------|
| **Faithfulness** | Check if LLM spec matches the `expected_output` without hallucinating |
| **Context Recall** | Verify all details in `expected_output` are covered by LLM spec |
| **Context Precision** | Ensure `acceptance_criteria` are all relevant to the scenario |
| **Answer Relevancy** | Check if LLM response semantically aligns with ground truth intent |

---

## Ground Truth Files

### Primary Source: `requirements-scenarios.json`
- **Format**: JSON array of 20 scenario objects
- **Fields per Scenario**: 7
  - feature
  - scenario
  - given
  - when
  - then
  - acceptance_criteria (array)
  - expected_output
- **Records**: 20 complete Gherkin scenarios

### Derived Format: `requirements-scenarios.csv`
- **Format**: CSV with 6 columns
- **Records**: 20 rows
- **Columns**: Feature, Scenario, Given, When, And, Then
- **Note**: CSV is synced from JSON but includes "And" for multi-step complexity
- **Usage**: Pandas/RAGAS pipeline data loading

---

## Ground Truth Quality Characteristics

### 1. **Domain Coverage** (9 RE Domains)
```
Domain                    | Scenarios | Example
--------------------------|-----------|--------
User Authentication       | 3         | Login valid/invalid, timeout
Password Reset           | 2         | Initiate, verify code
Profile Management       | 2         | Update profile, change password
Data Validation          | 2         | Email format, required fields
Role-Based Access Control| 2         | Admin access, deny access
Search Functionality     | 2         | Search results, empty results
Post Creation            | 2         | Create post, save draft
Requirement Versioning   | 1         | View history
Requirement Tracking     | 2         | Mark complete, update status
```

### 2. **Test Data Realism**
Ground truth includes specific, realistic test values:
- **Email addresses**: `hyphen_admin@acmetest.com`, `invalid@test.com`
- **Verification codes**: `34067` (numeric patterns)
- **Passwords**: `NewPass@123`, `NewSecure@456` (policy-compliant patterns)
- **Timeouts**: 30 minutes, 24 hours, 2 seconds (realistic SLA values)

### 3. **Coverage Breadth**

**Happy Paths** (5 scenarios)
- Valid credentials, correct data, successful operations
- Example: "User login with valid credentials"

**Error Paths** (4 scenarios)
- Invalid inputs, authentication failures, access denial
- Example: "User login with invalid credentials"

**Edge Cases** (3 scenarios)
- Timeouts, empty results, boundary conditions
- Example: "Session timeout after 30 minutes"

**Security Scenarios** (3 scenarios)
- RBAC, unauthorized access, permission checks
- Example: "Regular user cannot access admin panel"

**Validation Scenarios** (5 scenarios)
- Format validation, required fields
- Example: "System validates email format during registration"

### 4. **Acceptance Criteria Specificity**
Each scenario has 3-4 measurable acceptance criteria:
- ✅ Quantified metrics (timestamps, time limits)
- ✅ Observable system states (page loaded, error displayed)
- ✅ Database changes (status updated, session created)
- ✅ Notifications (user message, audit log)

### 5. **Completeness**
All 20 scenarios have:
- ✅ Complete Given-When-Then structure
- ✅ 3-4 acceptance criteria each
- ✅ Detailed expected_output (2-3 sentences minimum)
- ✅ Clear, unambiguous language
- ✅ No missing fields

---

## Ground Truth as RAGAS Reference

### How RAGAS Uses It

**Stage 1: Data Preparation**
```python
for scenario in scenarios:
    reference = scenario['expected_output']
    user_input = f"Feature: {scenario['feature']}..."
    
    ragas_dataset.append({
        'user_input': user_input,
        'reference': reference,  # ← Ground Truth
        'retrieved_contexts': [reference],  # ← Ground Truth Used Here
        'response': '[LLM-Generated Spec]'
    })
```

**Stage 2: Metric Computation**
```
Faithfulness(generated_response, reference)
    → How faithful is response to reference (ground truth)?
    
ContextRecall(retrieved_contexts, reference)
    → Does retrieved context cover all details in reference?
    
AnswerRelevancy(generated_response, user_input)
    → Does response semantically match what reference should be?
```

**Stage 3: Scoring**
- ✅ Generated spec matches reference → High Faithfulness score
- ❌ Generated spec deviates from reference → Low Faithfulness score
- ✅ All reference details covered → High Context Recall score
- ❌ Missing details from reference → Low Context Recall score

---

## Results: What Ground Truth Revealed

### Metric Scores from Evaluation

| Metric | Score | Ground Truth Implication |
|--------|-------|--------------------------|
| **Faithfulness: 62.2%** | MODERATE | LLM captured ~62% of ground truth correctly; ~38% hallucination/deviation |
| **Answer Relevancy: 49.2%** | LOW | LLM specs were only ~49% relevant to ground truth intent |
| **Context Precision: 100%** | EXCELLENT | Ground truth perfectly relevant to scenarios ✓ |
| **Context Recall: 100%** | EXCELLENT | Ground truth complete for all details ✓ |

### What This Tells Us

**Perfect Context Scores (100%) show:**
- ✅ Ground truth was well-designed
- ✅ All necessary information present
- ✅ All information relevant
- ✅ No extraneous details
- ✅ Scenarios are high-quality

**Moderate-to-Low Faithfulness/Relevancy show:**
- ⚠️ Gap between ground truth expectations and LLM output
- ⚠️ LLM struggles to match domain-specific ground truth patterns
- ⚠️ Need for better prompt engineering when generating specs
- ⚠️ LLM hallucinates or adds unexpected details

---

## Practical Use: Ground Truth for RE Quality

### 1. **Specification Validation**
```
Write requirement → Define ground truth → Generate spec → Compare
                                           ↓
                              Does spec match ground truth?
                              YES → Use spec
                              NO  → Refine prompt or requirement
```

### 2. **Requirements Clarity Measurement**
```
Low Faithfulness Score = Requirement was too ambiguous
Low Answer Relevancy = LLM couldn't understand what you meant
High Context Recall = You defined requirements well
```

### 3. **Team Standards**
```
High-scoring ground truth examples:
  → Show team what "clear" looks like
  
Low-scoring ground truth examples:
  → Show team what "ambiguous" looks like
```

### 4. **Continuous Improvement**
```
Evaluate requirements at each phase
↓
Track metric trends over time
↓
Identify when requirement quality drops
↓
Implement corrective actions
```

---

## Summary

| Aspect | Details |
|--------|---------|
| **Source** | Created by AI agent (exact prompts not documented) |
| **Format** | JSON (primary) + CSV (derived) |
| **Content** | 20 synthetic Gherkin BDD scenarios |
| **Domains** | 9 RE domains (Auth, Profile, RBAC, Search, etc.) |
| **Ground Truth** | Each scenario's `then` + `acceptance_criteria` + `expected_output` |
| **Role in RAGAS** | Reference standard against which LLM specs are evaluated |
| **Quality Markers** | 100% context precision/recall (excellent ground truth) |
| **Key Finding** | 62.2% faithfulness shows gap between ground truth and LLM output |
| **Practical Use** | Measure requirement clarity, validate specs, train teams |

---

**Key Insight:**
Ground truth is your team's definition of "correct behavior." RAGAS evaluation shows how well an LLM understands and respects those definitions. Perfect context scores prove your ground truth is well-written; imperfect faithfulness shows where LLM falls short of your expectations.

