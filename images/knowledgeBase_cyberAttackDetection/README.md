# knowledgeBase_cyberAttackDetection

## Image Information

- **Author:** Vaishnavi Vijaya
- **Course:** M. Grum: Advanced AI-based Application Systems
- **Institution:** University of Potsdam – Junior Chair for Business Information Science (AI-based Application Systems)
- **Purpose:** Provide trained AI models for inference (knowledge base image)
- **License:** AGPL-3.0

---

## Overview

This Docker image acts as the **Knowledge Base** in the AI-CPS architecture.
It contains **only trained model artifacts** required at inference time.

**Contents:**

* `currentAiSolution.h5` – Trained ANN model
* `currentOlsSolution.pkl` – Trained OLS (logistic regression) model
* `scaler.pkl` – Feature scaler used during training

No datasets, training scripts, or evaluation logic are included in this image.

---

## Image Contents Location

When mounted, the artifacts are available at:

```
/tmp/knowledgeBase/
├── currentAiSolution.h5
├── currentOlsSolution.pkl
└── scaler.pkl
```

---

## Build Image

```bash
docker build -t knowledgebase_cyberattackdetection .
```

---

## Run Image

### Run (standalone – inspect contents)

```bash
docker run --rm knowledgebase_cyberattackdetection
```

### Run with shared volume (recommended)

```bash
docker volume create ai_system

docker run --rm \
  -v ai_system:/tmp \
  knowledgebase_cyberattackdetection
```

---

## Verify Contents

```bash
docker run --rm \
  -v ai_system:/tmp \
  knowledgebase_cyberattackdetection \
  ls /tmp/knowledgeBase
```

---

## Usage in Docker Compose

```yaml
services:
  knowledgebase:
    image: knowledgebase_cyberattackdetection
    volumes:
      - ai_system:/tmp

volumes:
  ai_system:
    external: true
```

---

## Notes

* This image is **read-only** and intended to be used by inference containers
* Model performance metrics are documented in the **documentation folder**
* Feature order and preprocessing must match the training configuration

---

## License

Licensed under the **AGPL-3.0 License**.

- Developed strictly for academic and educational purposes
- Part of the Advanced AI-based Application Systems (AIBAS) coursework
- Not intended for production deployment
- University of Potsdam · AIBAS Coursework 
