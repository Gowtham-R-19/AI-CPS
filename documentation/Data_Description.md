# 📊 Processed Dataset Documentation

## Overview

This directory contains the **cleaned, validated, and split datasets** used for training, evaluating, and testing the Cyber Attack Detection System (ANN and OLS).

> **Note:** All files in this folder are derived exclusively from the raw NSL-KDD dataset through a reproducible preprocessing pipeline and represent the **single source of truth** for all experimental results reported in the project.

---

## 📈 Dataset Summary

| Metric | Value |
|--------|-------|
| **Total Records** | 148,517 |
| **Feature Columns** | 41 |
| **Data Leakage Status** | ✅ None detected (verified via overlap checks) |

### Label Columns

- **`label`** - Original attack category
- **`label_binary`** - Binary classification (0 = normal, 1 = attack)
- **`label_multiclass`** - Attack family classification
- **`label_multiclass_encoded`** - Numeric encoding of attack families

### Input Feature Description (41)

The following features are used as **model inputs** during training
and inference.

| Feature Name | Description |
|-------------|-------------|
| duration | Length (in seconds) of the network connection |
| protocol_type | Transport protocol used (TCP, UDP, ICMP) |
| service | Network service on the destination |
| flag | Status flag of the connection |
| src_bytes | Bytes sent from source to destination |
| dst_bytes | Bytes sent from destination to source |
| land | Indicates whether source and destination IP are the same |
| wrong_fragment | Number of wrong fragments |
| urgent | Number of urgent packets |
| hot | Number of “hot” indicators |
| num_failed_logins | Number of failed login attempts |
| logged_in | Indicates successful login |
| num_compromised | Number of compromised conditions |
| root_shell | Indicates whether a root shell was obtained |
| su_attempted | Indicates whether `su` was attempted |
| num_root | Number of root accesses |
| num_file_creations | Number of file creation operations |
| num_shells | Number of shell prompts invoked |
| num_access_files | Number of access control file operations |
| num_outbound_cmds | Number of outbound FTP commands |
| is_host_login | Indicates host-based login |
| is_guest_login | Indicates guest login |
| count | Number of connections to the same host |
| srv_count | Number of connections to the same service |
| serror_rate | Percentage of SYN errors |
| srv_serror_rate | SYN error rate for the same service |
| rerror_rate | Percentage of REJ errors |
| srv_rerror_rate | REJ error rate for the same service |
| same_srv_rate | Percentage of connections to the same service |
| diff_srv_rate | Percentage of connections to different services |
| srv_diff_host_rate | Percentage of connections to different hosts |
| dst_host_count | Connections to the same destination host |
| dst_host_srv_count | Connections to the same service on destination host |
| dst_host_same_srv_rate | Same-service connection rate for destination host |
| dst_host_diff_srv_rate | Different-service connection rate for destination host |
| dst_host_same_src_port_rate | Same source-port connection rate |
| dst_host_srv_diff_host_rate | Different-host connection rate for same service |
| dst_host_serror_rate | SYN error rate for destination host |
| dst_host_srv_serror_rate | SYN error rate for destination host and service |
| dst_host_rerror_rate | REJ error rate for destination host |
| dst_host_srv_rerror_rate | REJ error rate for destination host and service |


### Label Columns (4)

The following columns are **excluded from model input** and used
only for supervision and evaluation.

| Column Name | Description |
|-------------|-------------|
| label | Original attack label (string-based) |
| label_binary | Binary classification label (0 = Normal, 1 = Attack) |
| label_multiclass | High-level attack category (normal, dos, probe, r2l, u2r) |
| label_multiclass_encoded | Numerical encoding of multi-class labels |

---

## 📁 Processed Data Descriptions

### 1. **joint_data_collection.csv**

The comprehensive, consolidated dataset containing all cleaned records and features.

| Property | Value |
|----------|-------|
| **Records** | 148,517 |
| **Purpose** | Master dataset for validation and statistics |
| **Contains** | All features and labels |
| **Use Case** | Dataset integrity checks and quality validation |

**Key Features:**
- Fully deduplicated and cleaned records
- All preprocessing transformations applied
- Complete feature set and all label variations

---

### 2. **training_data.csv**

Primary dataset used for model development and training.

| Property | Value |
|----------|-------|
| **Records** | 118,325 |
| **Purpose** | Model training (ANN and OLS) |
| **Split Ratio** | ~80% of total dataset |
| **Class Distribution** | Original imbalance maintained |

**Key Features:**
- Used for both ANN and OLS model training
- Preserves original class imbalance for realistic performance metrics
- No data leakage with test dataset

---

### 3. **test_data.csv**

Held-out evaluation dataset for final model performance assessment.

| Property | Value |
|----------|-------|
| **Records** | 29,582 |
| **Purpose** | Final model evaluation and performance reporting |
| **Split Ratio** | ~20% of total dataset |
| **Overlap Check** | ✅ Verified - No overlap with training data |

**Key Features:**
- Exclusively used for model evaluation
- All performance metrics are computed on this dataset
- Completely isolated from training data

---

### 4. **activation_data.csv**

Minimal validation dataset for inference pipeline testing.

| Property | Value |
|----------|-------|
| **Records** | 2 |
| **Purpose** | End-to-end inference pipeline validation |
| **Statistical Use** | ❌ Not intended for evaluation |
| **Scope** | Deployment and inference verification only |

**Key Features:**
- Intentionally minimal for quick pipeline validation
- Sample data for Docker and deployment scenarios
- Used to verify model inference execution paths

---

### 5. **preprocessing_stats.json**

Metadata file capturing the complete preprocessing pipeline state.

**Generated Contents:**
- Raw vs. cleaned record counts
- Final dataset split sizes
- Preprocessing execution timestamps
- Data transformation logs

**Purpose:**
- Reproducibility tracking
- ML integrity documentation
- Pipeline state verification

---

## ⚠️ Important Guidelines

### Performance Metrics
🔴 **All performance metrics** reported in project documentation are computed **exclusively** on `test_data.csv`

### Data Integrity
✅ **Data leakage verification** completed through overlap checks between training and test datasets

### Modification Protocol
Any changes to these files require re-execution of:
1. Dataset validation scripts
2. Overlap verification checks
3. Complete model training and evaluation pipeline

---

## 📋 Quick Reference

| File | Records | Purpose |
|------|---------|---------|
| `joint_data_collection.csv` | 148,517 | Complete dataset + validation |
| `training_data.csv` | 118,325 | Model training |
| `test_data.csv` | 29,582 | Model evaluation & reporting |
| `activation_data.csv` | 2 | Inference validation |
| `preprocessing_stats.json` | Metadata | Pipeline reproducibility |

---

## 🔗 Related Documentation

- [ML Integrity Guidelines](../../documentation/ML_Integrity.md)
- [Model Results & Metrics](../../documentation/MODEL_RESULTS.md)
- [Preprocessing Scripts](../../code/preprocessing/)
- [Raw Dataset Info](../raw/README.md)

Or start cleaning the main project README section by section
