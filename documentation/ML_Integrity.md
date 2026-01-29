# ML INTEGRITY & DATA LEAKAGE PREVENTION REPORT

**Project Title:** Cyber Attack Detection System  
**Course:** M. Grum – Advanced AI-based Application Systems  
**Institution:** University of Potsdam  
**Authors:** Gowtham Ramakrishna, Vaishnavi Vijaya  
**Academic Year:** 2025–2026  
**Last Updated:** January 2026

---

## 1. Document Purpose

This document records the identification, resolution, and prevention of a data leakage incident encountered during the development of the Cyber Attack Detection System.

It serves as a permanent reference to ensure scientific validity, reproducibility, and academic integrity of all reported model results.

---

## 2. Incident Summary

During early model development, overlapping samples were detected between the training and test datasets. This resulted in test data being exposed to the models during training, violating fundamental evaluation principles.

---

## 3. Detection Method

The issue was identified using a custom dataset overlap validation script.

**Command executed:**
```bash
python code/training/check_overlap.py
```

**Initial detection output (historical):**
```
Overlap rows found: >0
WARNING: Potential data leakage detected
```

All results generated prior to remediation were invalidated.

---

## 4. Root Cause Analysis

The data leakage was caused by improper dataset splitting without explicit enforcement of record uniqueness.

### Contributing factors
- Duplicate records in the original dataset
- Preprocessing performed before dataset separation
- Absence of post-split validation checks

---

## 5. Impact Assessment

### Technical Impact
- Artificially inflated accuracy, precision, recall, and ROC-AUC values
- Misleading generalization performance

### Academic Impact
- Results failed reproducibility and peer-review standards
- Immediate corrective action was required

---

## 6. Remediation Procedure

The following remediation steps were executed:

- **Step 1:** Recombined original training and test datasets into a unified dataset.
- **Step 2:** Removed all duplicate records to ensure uniqueness.
- **Step 3:** Performed a fresh stratified split based on binary labels.

**Command executed:**
```bash
python code/training/resplit_dataset.py
```

---

## 7. Final Dataset State (Verified)

| Property | Value |
|----------|-------|
| Dataset Name | NSL-KDD |
| Total Records | 148,517 |
| Feature Columns | 41 |
| Training Records | 118,325 |
| Testing Records | 29,582 |
| Activation Records | 2 |

---

## 8. Verification & Validation

Post-remediation validation was conducted using the same overlap check.

**Command executed:**
```bash
python code/training/check_overlap.py
```

**Final verification output:**
```
Overlap rows found: 0
No data leakage detected
Training and test sets are cleanly separated.
```

---

## 9. Enforced Integrity Policy

The following policy is mandatory for all training executions:

- Dataset overlap validation must be executed before training
- If overlap rows > 0:
  - Training must be stopped immediately
  - Dataset must be recombined, cleaned, and re-split
  - Validation must be repeated
- Training is permitted only when overlap = 0

---

## 10. Code-Level Safeguards

A mandatory integrity notice is embedded at the beginning of training scripts (`train_ann.py`, `train_ols.py`):

### DATA INTEGRITY NOTICE

**Before training, verify:**
```bash
python code/training/check_overlap.py

```
**Expected:**
Overlap rows found: 0

---

## 11. Cause → Effect → Fix Summary

### Cause
- Improper dataset splitting and duplicate records

### Effect
- Test samples leaked into training data
- Inflated model performance metrics

### Fix
- Dataset recombination
- De-duplication
- Stratified re-splitting
- Mandatory overlap validation

### Prevention
- Enforced pre-training validation checks
- Code-level safeguards
- Centralized integrity documentation

---

## 12. Academic Integrity Statement

A dataset integrity issue involving overlapping samples between training and test sets was identified and resolved by recombining, de-duplicating, and stratifying the dataset prior to retraining. A mandatory post-split validation check is now enforced to prevent data leakage and ensure the scientific validity of all reported performance metrics.

---

## 13. Status

| Item | Status |
|------|--------|
| Dataset Integrity | Verified |
| Overlap Detection | None detected |
| Reproducibility | Guaranteed |
| Academic Compliance | Satisfied |

---

