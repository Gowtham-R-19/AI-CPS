# 🔒 Network Intrusion Detection Using Artificial Neural Networks

**Master's Thesis Project**  
**Course:** M. Grum: Advanced AI-based Application Systems  
**Institution:** Junior Chair for Business Information Science, esp. AI-based Application Systems, University of Potsdam  
**Team Members:** G & V  
**Academic Year:** 2025-2026

---

## 📋 Project Overview

This project implements an AI-based Network Intrusion Detection System (IDS) using Artificial Neural Networks (ANN) to detect cyber attacks with >90% accuracy. The system analyzes network traffic patterns to classify connections as normal or malicious (DoS, Probe, R2L, U2R).

**Expected Accuracy:** 92-98% (Binary Classification)  
**Dataset:** NSL-KDD (148,517 records, 41 features)  
**License:** AGPL-3.0

---

## 🎯 Project Objectives

1. **Primary Goal:** Build an AI system that detects network intrusions with >90% accuracy
2. **Secondary Goals:**
   - Compare ANN performance vs OLS baseline
   - Analyze feature importance in attack detection
   - Visualize attack patterns
   - Deploy via Docker containers

---

## 🗂 Repository Structure

```
AI-CPS/
├── code/                          # All source code
│   ├── scraping/                 # Web scraping scripts
│   ├── preprocessing/            # Data cleaning and preparation
│   ├── training/                 # Model training scripts
│   └── inference/                # Model inference scripts
├── data/                          # All datasets
│   ├── raw/                      # Original scraped data
│   └── processed/                # Cleaned and split data
│       ├── joint_data_collection.csv
│       ├── training_data.csv
│       ├── test_data.csv
│       └── activation_data.csv
├── documentation/                 # Project documentation
│   └── Final_Team_Report.pdf
├── images/                        # Docker images
│   ├── learningBase_cyberAttackDetection/
│   ├── activationBase_cyberAttackDetection/
│   ├── knowledgeBase_cyberAttackDetection/
│   └── codeBase_cyberAttackDetection/
└── scenarios/                     # Docker compose files
    ├── apply_annSolution_cyberAttackDetection/
    └── apply_olsSolution_cyberAttackDetection/
```

---

## 📊 Dataset Information

### NSL-KDD Dataset
**Source:** University of New Brunswick (UNB), Canadian Institute for Cybersecurity  
**URL:** https://www.unb.ca/cic/datasets/nsl.html  
**License:** ✅ Open Source - Academic Use Permitted  
**GDPR Compliant:** ✅ Synthetic network traffic (no personal data)

**Citation:**
```
Tavallaee, M., Bagheri, E., Lu, W., & Ghorbani, A. A. (2009).
A detailed analysis of the KDD CUP 99 data set.
IEEE Symposium on Computational Intelligence for Security and Defense Applications.
```

**Dataset Composition:**
- Total Records: 148,517
- Features: 41 + 1 label
- Training Set: 125,973 records
- Testing Set: 22,544 records
- Attack Types: Normal, DoS, Probe, R2L, U2R

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- Git
- 8GB RAM minimum

### Installation

1. **Clone this repository:**
```bash
git clone https://github.com/YourUsername/AI-CPS.git
cd AI-CPS
```

2. **Create Python virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create Docker volume:**
```bash
docker volume create ai_system
```

---

## 📈 Project Roadmap

### ✅ Subgoal 1: Git Usage (Week 1)
- [x] Fork AI-CPS repository
- [x] Set up team collaboration
- [x] Create initial README
- [ ] Make 3 commits per team member

### 🔄 Subgoal 2: Data Scraping & Preparation (Week 2)
- [ ] Scrape NSL-KDD dataset from web
- [ ] Clean and preprocess data
- [ ] Create training/test/activation splits
- [ ] Generate CSV files

### 🔄 Subgoal 3: Docker Data Provision (Week 3)
- [ ] Build learningBase image
- [ ] Build activationBase image
- [ ] Publish to Docker Hub
- [ ] Test with docker-compose

### 🔄 Subgoal 4: ANN Model Creation (Week 4)
- [ ] Design neural network architecture
- [ ] Train model with TensorFlow
- [ ] Generate visualizations
- [ ] Achieve >90% accuracy

### 🔄 Subgoal 5: OLS Baseline Model (Week 4)
- [ ] Implement logistic regression
- [ ] Compare with ANN performance
- [ ] Generate diagnostic plots

### 🔄 Subgoal 6: Docker Model Provision (Week 5)
- [ ] Build knowledgeBase image
- [ ] Build codeBase image
- [ ] Publish to Docker Hub
- [ ] Test inference pipeline

### 🔄 Subgoal 7: Docker Compose Integration (Week 6)
- [ ] Create docker-compose files
- [ ] Test end-to-end pipeline
- [ ] Final documentation

---

## 🐳 Docker Images

All images will be published at Docker Hub:

1. **learningBase_cyberAttackDetection**  
   - Contains: training_data.csv, test_data.csv
   - Pull: `docker pull username/learningBase_cyberAttackDetection`

2. **activationBase_cyberAttackDetection**  
   - Contains: activation_data.csv
   - Pull: `docker pull username/activationBase_cyberAttackDetection`

3. **knowledgeBase_cyberAttackDetection**  
   - Contains: Trained models (.h5, .pkl)
   - Pull: `docker pull username/knowledgeBase_cyberAttackDetection`

4. **codeBase_cyberAttackDetection**  
   - Contains: Inference scripts
   - Pull: `docker pull username/codeBase_cyberAttackDetection`

---

## 🔬 Expected Results

### ANN Model Performance
- **Binary Classification:** 94-98% accuracy
- **Multi-class Classification:** 87-93% accuracy
- **Training Time:** 10-15 minutes
- **Inference Time:** <10ms per sample

### OLS Baseline Performance
- **Binary Classification:** 75-82% accuracy
- **ANN Improvement:** +12-16% over OLS

---

## 📚 References

1. Tavallaee, M., Bagheri, E., Lu, W., & Ghorbani, A. A. (2009). A detailed analysis of the KDD CUP 99 data set. IEEE Symposium on Computational Intelligence for Security and Defense Applications.

2. NSL-KDD Dataset: https://www.unb.ca/cic/datasets/nsl.html

3. Grum, M. (2022). Construction of a Concept of Neuronal Modeling. Springer Gabler Wiesbaden.

---

## 👥 Team Contributions

### G (Team Member 1)
- Data acquisition and scraping
- Data preprocessing
- Docker data images
- Documentation

### V (Team Member 2)
- ANN model development
- OLS baseline model
- Docker model images
- Visualizations

---

## 📝 License

This project is licensed under the **AGPL-3.0 License** in accordance with the AI-CPS repository.

**Attribution Required:**
- This project was created as part of the course "M. Grum: Advanced AI-based Application Systems"
- Junior Chair for Business Information Science, esp. AI-based Application Systems
- University of Potsdam, Germany
- Dataset from UNB Canadian Institute for Cybersecurity

---

## 🔗 Important Links

- **GitHub Repository:** [Link will be added]
- **Docker Hub:** [Link will be added]
- **Course:** M. Grum: Advanced AI-based Application Systems
- **University:** https://www.uni-potsdam.de/

---

## 📞 Contact

For questions or issues, please contact:
- **G:** [email]
- **V:** [email]

**Submission Deadline:** February 5, 2026, 10:00 AM

---

## ⚠️ Important Notes

- This is an academic project for research purposes only
- All datasets used are open-source and GDPR compliant
- No commercial use without permission
- Follow university academic integrity policies

---

**Last Updated:** January 5, 2026  
**Status:** 🔄 In Progress - Subgoal 1 (Day 1)
