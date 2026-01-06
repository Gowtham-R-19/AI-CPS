# learningBase_cyberAttackDetection

## Image Information

**Owners:** G & V  
**Course:** M. Grum: Advanced AI-based Application Systems  
**Institution:** Junior Chair for Business Information Science, esp. AI-based Application Systems, University of Potsdam  
**Purpose:** Provide training and validation data for network intrusion detection system  
**License:** AGPL-3.0

---

## Data Origin

**Dataset:** NSL-KDD (Network Security Laboratory - Knowledge Discovery in Databases)  
**Source:** University of New Brunswick (UNB), Canadian Institute for Cybersecurity  
**URL:** https://www.unb.ca/cic/datasets/nsl.html  
**License:** Open Source - Academic Use Permitted  
**GDPR Compliance:** ✅ Synthetic network traffic data (no personal information)

**Citation:**
```
Tavallaee, M., Bagheri, E., Lu, W., & Ghorbani, A. A. (2009).
A detailed analysis of the KDD CUP 99 data set.
IEEE Symposium on Computational Intelligence for Security and Defense Applications.
```

---

## Image Contents

### File Structure
```
/tmp/learningBase/
├── train/
│   └── training_data.csv      (118,813 records - 80% of dataset)
├── validation/
│   └── test_data.csv           (29,704 records - 20% of dataset)
└── README.md
```

### Data Specifications

**training_data.csv:**
- Records: 118,813 (80% of joint dataset)
- Features: 41 numerical/categorical features
- Labels: Binary (normal=0, attack=1) + Multi-class (5 types)
- Size: ~28 MB
- Format: CSV with headers
- Preprocessing: Cleaned, encoded, normalized (Min-Max 0-1)

**test_data.csv:**
- Records: 29,704 (20% of joint dataset)
- Features: Same 41 features as training
- Labels: Binary + Multi-class
- Size: ~7 MB
- Format: CSV with headers
- Preprocessing: Same as training data
- Stratification: Maintains same attack/normal ratio as training

### Features (41 total)

**Basic Connection Features (9):**
1. duration, protocol_type, service, flag
2. src_bytes, dst_bytes, land, wrong_fragment, urgent

**Content Features (13):**
3. hot, num_failed_logins, logged_in, num_compromised
4. root_shell, su_attempted, num_root, num_file_creations
5. num_shells, num_access_files, num_outbound_cmds
6. is_host_login, is_guest_login

**Time-based Traffic Features (9):**
7. count, srv_count, serror_rate, srv_serror_rate
8. rerror_rate, srv_rerror_rate, same_srv_rate
9. diff_srv_rate, srv_diff_host_rate

**Host-based Features (10):**
10. dst_host_* features (10 statistical patterns)

**Labels:**
- label_binary: 0 (normal), 1 (attack)
- label_multiclass_encoded: 0 (normal), 1 (dos), 2 (probe), 3 (r2l), 4 (u2r)

---

## Usage

### Pull Image
```bash
docker pull [your-dockerhub-username]/learningbase_cyberattackdetection
```

### Run Image
```bash
# View contents
docker run --rm [your-dockerhub-username]/learningbase_cyberattackdetection

# Mount to external volume
docker run --rm -v ai_system:/tmp [your-dockerhub-username]/learningbase_cyberattackdetection

# Access files from another container
docker run --rm -v ai_system:/tmp your-training-container
# Files will be available at /tmp/learningBase/train/ and /tmp/learningBase/validation/
```

### Use with Docker Compose
```yaml
version: '3.8'
services:
  learning:
    image: [your-dockerhub-username]/learningbase_cyberattackdetection
    volumes:
      - ai_system:/tmp

volumes:
  ai_system:
    external: true
```

---

## Data Quality Metrics

- **Completeness:** 100% (no missing values)
- **Duplicates:** 0 (all removed during preprocessing)
- **Normalization:** All numerical features scaled to [0,1] using Min-Max scaler
- **Encoding:** Categorical features encoded using Label Encoding
- **Stratification:** Train/test split maintains attack distribution
- **Validation:** All records validated for data type consistency

---

## Attack Type Distribution

**Binary Classification:**
- Normal Traffic: ~45%
- Malicious Traffic: ~55%

**Multi-class Classification:**
- Normal: ~45%
- DoS (Denial of Service): ~31%
- Probe (Port Scanning): ~8%
- R2L (Remote to Local): ~1%
- U2R (User to Root): ~0.5%

---

## Integration with AI Models

This data is designed to be used with:
1. **ANN Model** (TensorFlow/Keras) - Subgoal 4
2. **OLS Baseline Model** (Logistic Regression) - Subgoal 5

Expected Model Performance:
- ANN: 92-98% accuracy (binary classification)
- OLS: 75-82% accuracy (binary classification)

---

## Version Information

**Data Version:** 1.0  
**Image Version:** 1.0  
**Created:** January 2026  
**Last Updated:** January 2026

---

## License & Attribution

This image and its contents are licensed under the **AGPL-3.0 license**.

**Required Attribution:**
- Dataset: NSL-KDD from UNB Canadian Institute for Cybersecurity
- Course: M. Grum: Advanced AI-based Application Systems
- Institution: University of Potsdam, Germany
- Created by: G & V (Team Members)

**Academic Use Only:** This image is created for educational and research purposes as part of a Master's thesis project.

---

## Contact & Support

**GitHub Repository:** [Add your GitHub URL]  
**Docker Hub:** [Add your Docker Hub URL]  
**Course:** M. Grum: Advanced AI-based Application Systems  
**Institution:** University of Potsdam

For questions or issues, please refer to the project documentation or contact the team members.

---

**Note:** This image is part of a larger cyber-physical system for AI-based intrusion detection. It must be used in conjunction with knowledge base (models) and code base (inference) images for complete functionality.
