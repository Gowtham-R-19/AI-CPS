# DATA LEAKAGE INCIDENT LOG & PREVENTION PROTOCOL

**Project:** AI-CPS — Cyber Attack Detection System  
**Course:** M. Grum: Advanced AI-based Application Systems  
**University:** University of Potsdam  
**Maintainer:** Gowtham R  
**Last Updated:** 2026-01-27

---

## 1. PURPOSE

This document records a critical dataset integrity issue discovered during ANN and OLS model training. It serves as a long-term reference for:

- What happened
- Why it mattered
- What impact it had on results
- How it was fixed
- What must be done in the future to prevent recurrence

## 2. INCIDENT SUMMARY

During a routine validation step, overlapping rows were found between the training and test datasets.

This means some samples used for testing were already seen by the model during training.

## 3. DETECTION METHOD

**Command used:**

```bash
python code/training/check_overlap.py
```

**Initial Output:**

```
Overlap rows found: 173
WARNING: Potential data leakage detected
```

## 4. ROOT CAUSE

The dataset was split into training and test sets without properly removing duplicate records or validating separation.

This can occur when:
- Data is preprocessed before splitting
- The original dataset contains duplicates
- The split process does not enforce uniqueness

## 5. IMPACT

### Technical Impact
- Model performance metrics were artificially inflated
- Accuracy, Precision, Recall, F1-score, and ROC-AUC appeared higher than true generalization performance

### Academic Impact
- Results were not scientifically valid
- Findings would fail reproducibility and peer-review standards

## 6. REMEDIATION ACTIONS

**Step 1:** Recombined training and test datasets into a single unified dataset.

**Step 2:** Removed all duplicate rows to ensure each sample is unique.

**Step 3:** Performed a stratified re-split based on label_binary to preserve class distribution across training and test sets.

**Command used:**

```bash
python code/training/resplit_dataset.py
```

## 7. VERIFICATION

**Validation Command:**

```bash
python code/training/check_overlap.py
```

**Final Output:**

```
Overlap rows found: 0
No data leakage detected
Training and test sets are cleanly separated.
```

## 8. LONG-TERM POLICY

Before running ANY training script, the overlap check must be executed.

**Mandatory rule:**
- If overlap rows > 0
  - STOP training
  - Re-split and clean dataset
  - Re-run overlap check
  - Only proceed when overlap = 0

## 9. CODE-LEVEL SAFEGUARD

The following reminder is added at the top of train_ann.py:

```
==========================================================
DATA INTEGRITY NOTICE
Before training, verify:
  python code/training/check_overlap.py
Expected:
  Overlap rows found: 0
==========================================================
```

## 10. CAUSE → EFFECT → FIX SUMMARY

| Aspect | Description |
|--------|-------------|
| **Cause** | Duplicate or improperly split data |
| **Effect** | Test samples appeared in training data, inflating model performance |
| **Fix** | Recombine, de-duplicate, and stratify before splitting |
| **Prevention** | Mandatory overlap validation before every training run |

## 11. ACADEMIC STATEMENT (REUSABLE)

A data integrity issue involving overlapping samples between training and test sets was identified and resolved by recombining, de-duplicating, and stratifying the dataset prior to retraining. A mandatory post-split validation check is now enforced to prevent data leakage and ensure scientific validity of all reported performance metrics.

## 12. STATUS

| Item | Status |
|------|--------|
| **Current State** | Dataset validated |
| **Overlap Detection** | No overlap detected |
| **Integrity** | Model training and evaluation are scientifically sound |