# 🔐 Cyber Attack Detection System using ANN and OLS

- **Course:** M. Grum – Advanced AI-based Application Systems - Data Science and Business Analytics
- **Instructor:** Prof. Dr. Marcus Grum  
- **Chair:** Junior Chair for Business Information Science, especially AI-based Application Systems  
- **Institution:** University of Potsdam, Germany  
- **Authors:**   Gowtham Ramakrishna, Vaishnavi Vijaya

---

## 📌 Project Overview

This project presents an AI-based **Cyber Attack Detection System** developed as part of the coursework for *Advanced AI-based Application Systems (AIBAS)* at the University of Potsdam.

The system applies **Artificial Neural Networks (ANN)** as a non-linear classifier and **Ordinary Least Squares (OLS)** as a linear baseline to detect malicious network traffic. The project emphasizes **reproducibility, data integrity, structured experimentation, and deployable system design**.

The work demonstrates the complete AI lifecycle:
- Dataset acquisition and validation  
- Data preprocessing and feature engineering  
- Model training and evaluation  
- Integrity and leakage validation  
- Containerized deployment and inference  
- Interpretable prediction outputs  

---

## 🎯 Objectives

- Build an AI-based intrusion detection system  
- Compare ANN and OLS models under identical conditions  
- Ensure experimental reproducibility and integrity  
- Enable containerized inference via Docker Compose  
- Provide auditable and interpretable predictions  

---

## 📊 Dataset

### NSL-KDD Dataset

This project is based on the **NSL-KDD** dataset, a refined benchmark dataset for network intrusion detection research.

- **Original Provider:**  
  University of New Brunswick (UNB), Canadian Institute for Cybersecurity  
- **Reference Page:**  
  https://www.unb.ca/cic/datasets/nsl.html  

At the time of development, the dataset was not directly downloadable from the original source in a machine-accessible format.  
Therefore, a **publicly available Kaggle mirror** was used to obtain the dataset in a reproducible manner.

- **Kaggle Dataset Source:**  
  https://www.kaggle.com/datasets/hassan06/nslkdd  

The dataset is **synthetic**, **GDPR-compliant**, and widely used for academic and educational research.

---

## 🧠 Modeling Approach

### Artificial Neural Network (ANN)
- Feed-forward neural network implemented using TensorFlow/Keras  
- Binary classification (Normal vs Attack)  
- Dropout-based regularization  
- Optimized for strong generalization performance  

### Ordinary Least Squares (OLS)
- Linear baseline classifier  
- Provides a transparent and computationally efficient reference  
- Highlights trade-offs between complexity and performance  

Both models share the same preprocessing pipeline and feature space to ensure fair comparison.

---

## 🐳 System Architecture (High Level)

The system is composed of four Docker-based components:

- **learningBase** – training and testing datasets  
- **activationBase** – activation (inference) dataset  
- **knowledgeBase** – trained models and preprocessing artifacts  
- **codeBase** – inference logic and prediction pipeline  

All components are orchestrated using **Docker Compose** to enable end-to-end execution.

---

## 🚀 Getting Started

### 1️⃣ Fork and Clone the Repository

```bash
git clone https://github.com/Gowtham-R-19/AI-CPS.git
cd AI-CPS
```

### 2️⃣ Python Environment (Optional – for local analysis)

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

Install required Python packages:

```bash
pip install -r requirements.txt
```

This step is required only if you want to run training, evaluation, or analysis locally.

### 3️⃣ Docker Prerequisites

Ensure Docker and Docker Compose are installed.

Verify installation:

```bash
docker --version
docker compose version
```

### 4️⃣ Create Docker Volume (Required)

A shared Docker volume is used for communication between containers.

```bash
docker volume create ai_system
```
## ▶️ Running Inference with Docker Compose

### 🔹 ANN-Based Inference

```bash
cd scenarios/apply_annSolution_cyberAttackDetection
docker compose up
```

This will:

```
- Load the trained ANN model
- Apply preprocessing
- Run inference on activation data
- Display predictions and confidence levels in the terminal
```

### 🔹 OLS-Based Inference

```bash
cd scenarios/apply_olsSolution_cyberAttackDetection
docker compose up
```

This executes the same pipeline using the OLS baseline model.

## 📊 Viewing Inference Results

Inference results are printed directly in the terminal and include:

```
- Prediction (Normal / Attack)
- Confidence score
- Risk-level interpretation
- End-to-end inference status
```

Each pipeline exits cleanly after completion.

## 📁 Repository Organization

The repository is organized into modular components:

```
data/        – raw and processed datasets
models/      – trained models and experiment runs
images/      – Docker image definitions
scenarios/   – Docker Compose deployment pipelines
documentation/ – integrity and results documentation
```

Each major directory contains (or will contain) its own dedicated README.md.

## 📜 License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).

## 📚 References & Tools

```
TensorFlow / Keras – https://www.tensorflow.org
Docker – https://www.docker.com
NSL-KDD (UNB) – https://www.unb.ca/cic/datasets/nsl.html
NSL-KDD (Kaggle Mirror) – https://www.kaggle.com/datasets/hassan06/nslkdd
University of Potsdam – https://www.uni-potsdam.de
```

## ℹ️ Notes

```
- Developed strictly for academic and educational purposes
- Part of the Advanced AI-based Application Systems (AIBAS) coursework
- Not intended for production deployment
- University of Potsdam · AIBAS Coursework 
```
