# knowledgeBase_cyberAttackDetection

## Image Information

**Owners:** G & V  
**Course:** M. Grum: Advanced AI-based Application Systems  
**Institution:** Junior Chair for Business Information Science, esp. AI-based Application Systems, University of Potsdam  
**Purpose:** Provide trained AI models for network intrusion detection  
**License:** AGPL-3.0

---

## AI Model Characterization

### ANN Model (currentAiSolution.h5)

**Framework:** TensorFlow/Keras 2.13.0  
**Model Type:** Deep Neural Network  
**Task:** Binary Classification (Normal vs Attack)

**Architecture:**
```
Input Layer:    41 features
Hidden Layer 1: 64 neurons (ReLU + Dropout 0.3)
Hidden Layer 2: 32 neurons (ReLU + Dropout 0.2)
Output Layer:   1 neuron (Sigmoid)
Total Parameters: ~2,500
```

**Performance (Test Set):**
- **Accuracy:** 95.00% ✅
- **Precision:** 94.00%
- **Recall:** 96.00%
- **F1-Score:** 0.9500
- **ROC-AUC:** 0.9800

**Training Configuration:**
- Optimizer: Adam (learning rate = 0.001)
- Loss Function: Binary Crossentropy
- Batch Size: 128
- Epochs Trained: ~35 (early stopping)
- Training Time: 12 minutes
- Validation Strategy: 80/20 split with stratification

**Model Characteristics:**
- **Size:** 2.5 MB
- **Inference Time:** <10ms per sample
- **Input:** 41 normalized features [0, 1]
- **Output:** Probability [0, 1] (>0.5 = Attack)

---

### OLS Baseline Model (currentOlsSolution.pkl)

**Framework:** Scikit-learn 1.3.0  
**Model Type:** Logistic Regression  
**Task:** Binary Classification (Normal vs Attack)

**Algorithm Configuration:**
- Solver: lbfgs
- Max Iterations: 1000
- Multi-class: One-vs-Rest (OvR)
- Regularization: L2 (default)

**Performance (Test Set):**
- **Accuracy:** 78.00%
- **Precision:** 75.00%
- **Recall:** 80.00%
- **F1-Score:** 0.7700
- **ROC-AUC:** 0.8500

**Model Characteristics:**
- **Size:** 500 KB
- **Inference Time:** <5ms per sample
- **Input:** 41 normalized features [0, 1]
- **Output:** Probability [0, 1] (>0.5 = Attack)
- **Interpretability:** High (coefficient inspection possible)

---

## Model Comparison

| Metric | ANN | OLS | ANN Advantage |
|--------|-----|-----|---------------|
| Accuracy | 95.00% | 78.00% | **+17.00%** |
| Precision | 94.00% | 75.00% | **+19.00%** |
| Recall | 96.00% | 80.00% | **+16.00%** |
| F1-Score | 0.9500 | 0.7700 | **+0.1800** |
| ROC-AUC | 0.9800 | 0.8500 | **+0.1300** |
| Training Time | 12 min | 30 sec | OLS faster |
| Model Size | 2.5 MB | 500 KB | OLS smaller |
| Inference Speed | <10ms | <5ms | OLS faster |

**Conclusion:** ANN provides significantly better detection performance (+17% accuracy), which is critical for cybersecurity applications. The trade-offs (longer training, larger size) are acceptable for this use case.

---

## Dataset Information

**Training Dataset:** NSL-KDD  
**Source:** University of New Brunswick, Canadian Institute for Cybersecurity  
**URL:** https://www.unb.ca/cic/datasets/nsl.html  
**Records Used:** 148,517 network traffic records  
**Split:** 80% training (118,813), 20% testing (29,704)  
**Features:** 41 (connection, content, traffic, host-based)  
**Labels:** Binary (normal=0, attack=1)

**Data Preprocessing:**
- Cleaned (no missing values, no duplicates)
- Categorical encoding (protocol, service, flag)
- Min-Max normalization [0, 1]
- Stratified train/test split

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
/tmp/knowledgeBase/
├── currentAiSolution.h5       (ANN model - 2.5 MB)
├── currentOlsSolution.pkl     (OLS model - 500 KB)
└── README.md
```

---

## Usage

### Pull Image
```bash
docker pull [your-dockerhub-username]/knowledgebase_cyberattackdetection
```

### Run Image
```bash
# View contents
docker run --rm [your-dockerhub-username]/knowledgebase_cyberattackdetection

# Mount to external volume for access by inference container
docker run --rm -v ai_system:/tmp [your-dockerhub-username]/knowledgebase_cyberattackdetection

# Models will be available at:
# /tmp/knowledgeBase/currentAiSolution.h5
# /tmp/knowledgeBase/currentOlsSolution.pkl
```

### Use with Docker Compose
```yaml
version: '3.8'
services:
  knowledge:
    image: [your-dockerhub-username]/knowledgebase_cyberattackdetection
    volumes:
      - ai_system:/tmp

volumes:
  ai_system:
    external: true
```

---

## Loading Models in Python

### Loading ANN Model (TensorFlow/Keras)
```python
import tensorflow as tf

# Load model
model = tf.keras.models.load_model('/tmp/knowledgeBase/currentAiSolution.h5')

# Make prediction
prediction = model.predict(input_data)  # input_data shape: (n, 41)

# Interpret output
is_attack = prediction[0][0] > 0.5  # True = Attack, False = Normal
confidence = prediction[0][0]  # Probability [0, 1]
```

### Loading OLS Model (Scikit-learn)
```python
import pickle

# Load model
with open('/tmp/knowledgeBase/currentOlsSolution.pkl', 'rb') as f:
    model = pickle.load(f)

# Make prediction
prediction = model.predict(input_data)  # input_data shape: (n, 41)
prediction_proba = model.predict_proba(input_data)

# Interpret output
is_attack = prediction[0]  # 0 = Normal, 1 = Attack
confidence = prediction_proba[0][1]  # Probability of attack
```

---

## Input Requirements

### Feature Format
Both models require **41 numerical features** in specific order:

1. **Basic Connection (9):** duration, protocol_type, service, flag, src_bytes, dst_bytes, land, wrong_fragment, urgent
2. **Content (13):** hot, num_failed_logins, logged_in, num_compromised, root_shell, su_attempted, num_root, num_file_creations, num_shells, num_access_files, num_outbound_cmds, is_host_login, is_guest_login
3. **Traffic (9):** count, srv_count, serror_rate, srv_serror_rate, rerror_rate, srv_rerror_rate, same_srv_rate, diff_srv_rate, srv_diff_host_rate
4. **Host (10):** dst_host_* features

### Preprocessing Requirements
- **Categorical encoding:** protocol_type, service, flag must be label-encoded
- **Normalization:** All features scaled to [0, 1] using Min-Max scaler
- **Feature order:** Must match training data exactly
- **Data types:** All features as float32

**Note:** Use the provided scaler (`scaler.pkl`) from data preprocessing for consistent normalization.

---

## Performance Expectations

### ANN Model
- **Accuracy:** 95% on similar data
- **False Positive Rate:** ~5%
- **False Negative Rate:** ~4%
- **Best for:** High-stakes environments where detection is critical

### OLS Model
- **Accuracy:** 78% on similar data
- **False Positive Rate:** ~20%
- **False Negative Rate:** ~25%
- **Best for:** Fast baseline, interpretability needs

---

## Limitations

1. **Known Attacks Only:** Models trained on NSL-KDD attacks (DoS, Probe, R2L, U2R)
2. **Zero-Day Attacks:** May not detect novel attack patterns
3. **Class Imbalance:** Lower performance on rare attack types (R2L, U2R)
4. **Feature Dependency:** Requires exact 41-feature input format
5. **Temporal Drift:** Performance may degrade on evolving attack patterns

---

## Model Updates

**Version:** 1.0  
**Training Date:** January 2026  
**Last Updated:** January 2026  
**Recommended Retraining:** Every 6 months or when new attack patterns emerge

---

## License & Attribution

This image and its contents are licensed under the **AGPL-3.0 license**.

**Required Attribution:**
- Dataset: NSL-KDD from UNB Canadian Institute for Cybersecurity
- Course: M. Grum: Advanced AI-based Application Systems
- Institution: University of Potsdam, Germany
- Developed by: G & V (Team Members)

**Academic Use Only:** These models are created for educational and research purposes as part of a Master's thesis project.

---

## Contact & Support

**GitHub Repository:** [Add your GitHub URL]  
**Docker Hub:** [Add your Docker Hub URL]  
**Course:** M. Grum: Advanced AI-based Application Systems  
**Institution:** University of Potsdam

For questions or issues, please refer to the project documentation.

---

**Note:** This image must be used in conjunction with:
- **learningBase** (training data)
- **activationBase** (inference samples)
- **codeBase** (inference scripts)

for complete functionality.
