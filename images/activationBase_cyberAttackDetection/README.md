# activationBase_cyberAttackDetection

## Image Information

**Owners:** G & V  
**Course:** M. Grum: Advanced AI-based Application Systems  
**Institution:** Junior Chair for Business Information Science, esp. AI-based Application Systems, University of Potsdam  
**Purpose:** Provide sample activation data for model inference testing  
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
/tmp/activationBase/
├── activation_data.csv    (2 sample records)
└── README.md
```

### Data Specifications

**activation_data.csv:**
- Records: 2 (1 normal traffic + 1 attack traffic)
- Features: 41 numerical/categorical features (same as training data)
- Labels: Binary + Multi-class
- Size: ~1 KB
- Format: CSV with headers
- Preprocessing: Same as training data (cleaned, encoded, normalized)
- Purpose: Demonstrate model inference on new data

### Sample Records

**Record 1:** Normal network traffic example
- Expected prediction: Class 0 (Normal)
- Confidence: >95%

**Record 2:** Attack traffic example
- Expected prediction: Class 1 (Attack)
- Attack type: [DoS/Probe/R2L/U2R]
- Confidence: >90%

---

## Usage

### Pull Image
```bash
docker pull [your-dockerhub-username]/activationbase_cyberattackdetection
```

### Run Image
```bash
# View contents
docker run --rm [your-dockerhub-username]/activationbase_cyberattackdetection

# Mount to external volume
docker run --rm -v ai_system:/tmp [your-dockerhub-username]/activationbase_cyberattackdetection

# Access files from inference container
docker run --rm -v ai_system:/tmp your-inference-container
# File will be available at /tmp/activationBase/activation_data.csv
```

### Use with Docker Compose
```yaml
version: '3.8'
services:
  activation:
    image: [your-dockerhub-username]/activationbase_cyberattackdetection
    volumes:
      - ai_system:/tmp

volumes:
  ai_system:
    external: true
```

---

## Integration with Inference Pipeline

This activation data is used to:
1. Test model inference functionality
2. Demonstrate real-time attack detection
3. Validate preprocessing pipeline
4. Verify model predictions

### Expected Inference Workflow
```
activation_data.csv
    ↓
Load & Preprocess
    ↓
Apply trained model (ANN or OLS)
    ↓
Get predictions + confidence scores
    ↓
Interpret results
    ↓
Output: Normal / Attack classification
```

---

## Features (41 total)

Same feature set as training/testing data:

**Connection Features:**
- duration, protocol_type, service, flag
- src_bytes, dst_bytes, land, wrong_fragment, urgent

**Content Features:**
- hot, num_failed_logins, logged_in, num_compromised
- root_shell, su_attempted, num_root, etc.

**Traffic Features:**
- count, srv_count, error rates, same service rates

**Host Features:**
- dst_host_count, dst_host_srv_count, etc.

All features are preprocessed (normalized to [0,1] range, categorical encoded).

---

## Use Cases

### 1. Model Testing
Test that trained models can:
- Load successfully
- Process input data
- Generate predictions
- Output confidence scores

### 2. Performance Validation
Verify that inference:
- Completes in <10ms per sample
- Produces correct predictions
- Handles both normal and attack traffic

### 3. Integration Testing
Ensure that:
- Data flows correctly through Docker volumes
- Preprocessing matches training pipeline
- Model outputs are properly formatted

### 4. Demonstration
Show stakeholders:
- How the system detects attacks
- Model confidence levels
- Real-time prediction capability

---

## Expected Model Performance

**ANN Model:**
- Normal traffic: 95-98% confidence (correct prediction)
- Attack traffic: 90-97% confidence (correct prediction)
- Inference time: <10ms per sample

**OLS Baseline:**
- Normal traffic: 80-85% confidence (correct prediction)
- Attack traffic: 75-82% confidence (correct prediction)
- Inference time: <5ms per sample

---

## Version Information

**Data Version:** 1.0  
**Image Version:** 1.0  
**Created:** January 2026  
**Last Updated:** January 2026  
**Sample Size:** 2 records (minimal for demonstration)

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

**Note:** This image is part of a larger cyber-physical system for AI-based intrusion detection. It must be used in conjunction with learning base (training data), knowledge base (models), and code base (inference) images for complete functionality.
