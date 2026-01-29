# MODEL RESULTS

**Project Title:** Cyber Attack Detection using Artificial Neural Networks 
**Course:** M. Grum – Advanced AI-based Application Systems  
**Institution:** University of Potsdam  
**Authors:** Gowtham Ramakrishna, Vaishnavi Vijaya  
**Academic Year:** 2025–2026  
**Date:** January 2026

---

## 1. Document Purpose

This document presents the **final, verified, and frozen results** of the Cyber Attack Detection system implemented using:

- Artificial Neural Networks (ANN)
- Ordinary Least Squares (OLS) Logistic Regression

All values reported in this document are:
- Extracted directly from repository artifacts
- Reproducible
- Verified
- Approved for academic submission

---

## 2. Execution Environment

| Component | Version |
|-----------|---------|
| Python | 3.11.3 |
| Docker | 28.5.1 (build e180ab8) |
| Docker Compose | v2.40.0-desktop.1 |
| Execution Mode | Local CPU (no GPU acceleration) |

---

## 3. Dataset Overview

| Property | Value |
|----------|-------|
| Dataset Name | NSL-KDD |
| Total Records | 148,517 |
| Total Columns | 45 |
| Feature Columns | 41 |

**Label Columns:**
- `label`
- `label_binary`
- `label_multiclass`
- `label_multiclass_encoded`

---

## 4. Data Splits (Final)

| Split | Records |
|-------|---------|
| Training Records | 118,325 |
| Testing Records | 29,582 |
| Activation Records | 2 |
| Data Leakage | None detected |
| Overlap Validation | 0 overlapping records |

---

## 5. Label Definitions

### Binary Classification
- `0` → Normal
- `1` → Attack

### Multi-class Categories
- `normal`
- `dos`
- `probe`
- `r2l`
- `u2r`

---


## 6. ANN Model — Architecture

| Property | Value |
|----------|-------|
| Framework | TensorFlow / Keras |
| Model Type | Sequential Artificial Neural Network |
| Input Features | 41 |
| Total Parameters | 4,801 |
| Trainable Parameters | 4,801 |
| Model Size (Disk) | ~0.086 MB |

### Architecture Layers
- Dense layer (64 units) + Dropout
- Dense layer (32 units) + Dropout
- Output layer (1 unit, Sigmoid)

---

## 7. ANN Model — Training Metrics (Latest Run)

| Metric | Value |
|--------|-------|
| Training Time | 148.62 seconds (~2.48 minutes) |
| Epochs Trained | 50 |
| Best Epoch | 41 |
| Training Accuracy | 98.88% |
| Validation Accuracy | 99.02% |

---

## 8. ANN Model — Test Performance

| Metric | Value |
|--------|-------|
| Test Accuracy | 98.89% |
| Precision | 98.71% |
| Recall | 98.97% |
| F1-Score | 98.84% |
| ROC-AUC | 0.99917 |

---

## 9. OLS Model — Training Metrics

| Property | Value |
|----------|-------|
| Model Type | Logistic Regression (OLS Baseline) |
| Training Time | 5.52 seconds |
| Model Size | ~0.001 MB |

---

## 10. OLS Model — Test Performance

| Metric | Value |
|--------|-------|
| Test Accuracy | 93.59% |
| Precision | 95.16% |
| Recall | 91.28% |
| F1-Score | 93.18% |
| ROC-AUC | 0.98175 |

---

## 11. ANN vs OLS Performance Comparison

### Accuracy Improvement
- **ANN over OLS:** ~5.29 percentage points

### Interpretation
- ANN provides superior detection performance
- OLS remains a strong, lightweight baseline
- Performance gains justify ANN complexity for security use cases

---

## 12. Docker Compose — Inference Validation

### ANN Inference
- **Activation Samples:** 2
- **Feature Count:** 41
- **Scaling:** StandardScaler
- **End-to-end Time:** ~450 ms
- **Predictions:**
  - Sample 1 → Normal (Very Low Risk)
  - Sample 2 → Attack (Critical Risk)
- **Container Exit Code:** 0 (Success)

### OLS Inference
- **Activation Samples:** 2
- **Feature Count:** 41
- **Scaling:** StandardScaler
- **End-to-end Time:** ~0.63 ms
- **Predictions:**
  - Sample 1 → Normal (Very Low Risk)
  - Sample 2 → Attack (Critical Risk)
- **Container Exit Code:** 0 (Success)

---

## 13. Visualizations (Latest Run)

Latest run: `run_2026-01-27_11-26-40`

### ANN Visualizations

- Training and validation curves
- ROC curve
- Precision–Recall curve
- Confusion matrix

### OLS Visualizations

- ROC curve
- Confusion matrix
- Residual plot
- Predicted vs actual
- ANN vs OLS comparison

---

## 14. Academic Conclusions

### Key Findings
- ANN achieves near-perfect binary intrusion detection
- ANN consistently outperforms OLS on all evaluation metrics
- Data integrity and leakage prevention significantly impact results

### Limitations
- Trained on known attack patterns (NSL-KDD)
- Rare attack classes remain challenging
- Concept drift may affect future performance

---

## 15. Status

All values in this document are:
- ✓ Verified from repository artifacts
- ✓ Frozen
- ✓ Approved for README and report usage
- ✓ Safe for academic submission

---
