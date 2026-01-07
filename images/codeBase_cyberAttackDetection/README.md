# codeBase_cyberAttackDetection

## Image Information

**Owners:** G & V  
**Course:** M. Grum: Advanced AI-based Application Systems  
**Institution:** Junior Chair for Business Information Science, esp. AI-based Application Systems, University of Potsdam  
**Purpose:** Provide inference code for network intrusion detection  
**License:** AGPL-3.0

---

## Image Contents

### File Structure
```
/app/
├── predict.py      (Inference script - 400+ lines)
└── README.md
```

### Dependencies Installed
- Python 3.9
- TensorFlow 2.13.0 (for ANN inference)
- Pandas 2.0.3 (data handling)
- NumPy 1.24.3 (numerical operations)
- Scikit-learn 1.3.0 (for OLS inference)

---

## Inference Script Features

### Core Functionality
1. **Model Loading:** Load trained ANN or OLS models from knowledge base
2. **Data Loading:** Load activation data for inference
3. **Preprocessing:** Apply same transformations as training
4. **Prediction:** Run inference and get predictions
5. **Interpretation:** Convert predictions to actionable insights
6. **Results Export:** Save predictions to JSON format

### Supported Models
- **ANN Model:** Deep neural network (95% accuracy)
- **OLS Model:** Logistic regression baseline (78% accuracy)

### Input/Output
- **Input:** CSV file with 41 network traffic features
- **Output:** JSON file with predictions, confidence scores, and recommendations

---

## Usage

### Pull Image
```bash
docker pull [your-dockerhub-username]/codebase_cyberattackdetection
```

### Run Inference (Standalone)
```bash
# Run with ANN model (default)
docker run --rm \
  -v ai_system:/tmp \
  [your-dockerhub-username]/codebase_cyberattackdetection \
  --model ann

# Run with OLS model
docker run --rm \
  -v ai_system:/tmp \
  [your-dockerhub-username]/codebase_cyberattackdetection \
  --model ols
```

### Use with Docker Compose
```yaml
version: '3.8'
services:
  knowledge:
    image: [your-dockerhub-username]/knowledgebase_cyberattackdetection
    volumes:
      - ai_system:/tmp

  activation:
    image: [your-dockerhub-username]/activationbase_cyberattackdetection
    volumes:
      - ai_system:/tmp

  inference:
    image: [your-dockerhub-username]/codebase_cyberattackdetection
    volumes:
      - ai_system:/tmp
    depends_on:
      - knowledge
      - activation
    command: ["--model", "ann"]

volumes:
  ai_system:
    external: true
```

---

## Inference Pipeline

### Step-by-Step Process

1. **Model Loading**
   - Loads trained model from `/tmp/knowledgeBase/`
   - ANN: `currentAiSolution.h5` (TensorFlow)
   - OLS: `currentOlsSolution.pkl` (Pickle)

2. **Data Loading**
   - Loads activation data from `/tmp/activationBase/activation_data.csv`
   - Validates input format (41 features required)

3. **Preprocessing**
   - Removes label columns if present
   - Applies normalization if needed (Min-Max [0,1])
   - Ensures feature order matches training

4. **Prediction**
   - Runs model inference
   - Generates probability scores
   - Converts to binary predictions (>0.5 threshold)

5. **Interpretation**
   - Classifies as Normal or Attack
   - Calculates confidence percentage
   - Determines severity level
   - Recommends actions

6. **Output**
   - Displays results to console
   - Saves to `predictions.json`

---

## Output Format

### Console Output Example
```
==============================================================
PREDICTION RESULTS
==============================================================

==============================================================
Sample #1
==============================================================
Verdict:     Normal Traffic
Prediction:  Normal
Confidence:  96.50%
Severity:    None
Action:      Continue monitoring

==============================================================
Sample #2
==============================================================
Verdict:     ATTACK DETECTED
Prediction:  Attack (DoS/Probe/R2L/U2R)
Confidence:  98.75%
Severity:    Critical
Action:      IMMEDIATE: Block source IP, isolate affected systems

==============================================================
SUMMARY
==============================================================
Total samples analyzed: 2
Normal traffic:         1 (50.0%)
Attacks detected:       1 (50.0%)
Average attack confidence: 98.75%
```

### JSON Output Example
```json
{
  "model_type": "ann",
  "timestamp": "2026-01-07T14:30:00",
  "total_samples": 2,
  "predictions": [
    {
      "sample_id": 1,
      "prediction": 0,
      "label": "Normal",
      "confidence": 0.9650,
      "confidence_percent": "96.50%",
      "verdict": "Normal Traffic",
      "severity": "None",
      "recommended_action": "Continue monitoring"
    },
    {
      "sample_id": 2,
      "prediction": 1,
      "label": "Attack (DoS/Probe/R2L/U2R)",
      "confidence": 0.9875,
      "confidence_percent": "98.75%",
      "verdict": "ATTACK DETECTED",
      "severity": "Critical",
      "recommended_action": "IMMEDIATE: Block source IP, isolate affected systems"
    }
  ]
}
```

---

## Severity Levels

### Classification

| Confidence | Severity | Action Required |
|------------|----------|-----------------|
| >95% | **Critical** | Immediate response |
| 85-95% | **High** | Urgent investigation |
| 70-85% | **Medium** | Enhanced monitoring |
| 50-70% | **Low** | Alert and review |

### Recommended Actions

**Critical (>95% confidence):**
- Block source IP immediately
- Isolate affected systems
- Initiate incident response protocol
- Notify security team

**High (85-95% confidence):**
- Investigate source and destination
- Prepare countermeasures
- Enhanced logging
- Alert security operations center

**Medium (70-85% confidence):**
- Enhanced monitoring of traffic
- Collect evidence for analysis
- Review firewall rules
- Correlate with other security events

**Low (50-70% confidence):**
- Review logs for patterns
- Verify with secondary detection systems
- Continue normal monitoring
- Document for trend analysis

---

## Performance Characteristics

### ANN Model Inference
- **Accuracy:** 95% (on test data)
- **Inference Time:** <10ms per sample
- **Memory Usage:** ~100 MB (model loaded)
- **Best For:** High-accuracy detection in production

### OLS Model Inference
- **Accuracy:** 78% (on test data)
- **Inference Time:** <5ms per sample
- **Memory Usage:** ~50 MB (model loaded)
- **Best For:** Fast baseline, resource-constrained environments

---

## Requirements

### Volume Mounting
Must mount `ai_system` volume containing:
- `/tmp/knowledgeBase/` - Trained models
- `/tmp/activationBase/` - Activation data
- `/tmp/learningBase/` - (Optional) Preprocessing artifacts

### Data Format
Input CSV must have:
- 41 numerical features (in correct order)
- Features normalized to [0, 1] range
- Optional: label columns (will be ignored)

---

## Error Handling

### Common Issues

**1. Model Not Found**
```
❌ Error loading ANN model: No such file or directory
```
**Solution:** Ensure knowledgeBase image is mounted to `ai_system` volume

**2. Activation Data Missing**
```
❌ Error loading activation data: activation_data.csv not found
```
**Solution:** Ensure activationBase image is mounted to `ai_system` volume

**3. TensorFlow Not Available**
```
Warning: TensorFlow not available. ANN inference will not work.
```
**Solution:** Use OLS model instead: `--model ols`

**4. Input Shape Mismatch**
```
❌ Error during prediction: Expected 41 features, got 40
```
**Solution:** Verify input data has all 41 required features

---

## Integration Examples

### With Docker Compose (Complete System)
```yaml
version: '3.8'
services:
  # Provide training data
  learning:
    image: yourusername/learningbase_cyberattackdetection
    volumes:
      - ai_system:/tmp

  # Provide activation samples
  activation:
    image: yourusername/activationbase_cyberattackdetection
    volumes:
      - ai_system:/tmp

  # Provide trained models
  knowledge:
    image: yourusername/knowledgebase_cyberattackdetection
    volumes:
      - ai_system:/tmp

  # Run inference
  inference:
    image: yourusername/codebase_cyberattackdetection
    volumes:
      - ai_system:/tmp
    depends_on:
      - learning
      - activation
      - knowledge
    command: ["--model", "ann"]

volumes:
  ai_system:
    external: true
```

### Python Integration
```python
import subprocess
import json

# Run inference via Docker
result = subprocess.run([
    'docker', 'run', '--rm',
    '-v', 'ai_system:/tmp',
    'yourusername/codebase_cyberattackdetection',
    '--model', 'ann'
], capture_output=True, text=True)

# Parse results
# (predictions.json will be in volume)
```

---

## Version Information

**Script Version:** 1.0  
**Python Version:** 3.9  
**TensorFlow Version:** 2.13.0  
**Created:** January 2026  
**Last Updated:** January 2026

---

## License & Attribution

This image and its contents are licensed under the **AGPL-3.0 license**.

**Required Attribution:**
- Course: M. Grum: Advanced AI-based Application Systems
- Institution: University of Potsdam, Germany
- Developed by: G & V (Team Members)

**Academic Use Only:** This inference code is created for educational and research purposes as part of a Master's thesis project.

---

## Contact & Support

**GitHub Repository:** [Add your GitHub URL]  
**Docker Hub:** [Add your Docker Hub URL]  
**Course:** M. Grum: Advanced AI-based Application Systems  
**Institution:** University of Potsdam

For questions or issues, please refer to the project documentation.

---

**Note:** This image is part of a complete cyber-physical system. It must be used with:
- **learningBase** (training/testing data)
- **activationBase** (inference samples)
- **knowledgeBase** (trained models)

for full functionality.
