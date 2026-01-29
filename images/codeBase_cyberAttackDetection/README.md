# codeBase_cyberAttackDetection

- Docker image that contains runtime inference logic for the AI-CPS intrusion detection pipeline.

---

## Image Information
- **Course:** M. Grum – Advanced AI-based Application Systems - Data Science and Business Analytics
- **Instructor:** Prof. Dr. Marcus Grum  
- **Chair:** Junior Chair for Business Information Science, especially AI-based Application Systems  
- **Institution:** University of Potsdam, Germany  
- **Authors:**   Vaishnavi Vijaya
- **Purpose:** Provide inference scripts that run ANN or OLS models against activation data
- **License:** AGPL-3.0
---

## 📌 Overview
This image packages the inference logic and utilities used during prediction. It is a lightweight, stateless image designed to:

- Run inference with pre-trained models (`ANN` or `OLS`)
- Read models from the **knowledgeBase** image (or shared volume)
- Read input/activation data from the **activationBase** image (or shared volume)
- Write prediction outputs to a shared Docker volume

This image intentionally does NOT contain:
- Trained model files (models are provided via a separate knowledge image or volume)
- Training datasets or training code

---

## 📁 Files inside the image
Path: `/app/`
- `predict.py` — inference entrypoint
- `README.md` — this file

The image's default behavior is to run the `predict.py` script when started.

---

## 🛠️ Build the image
From the `images/codeBase_cyberAttackDetection/` directory run:

```bash
docker build -t codebase_cyberattackdetection .
```

---

## ▶️ Run the image
Run with ANN model (default):

```bash
docker run --rm \
  -v ai_system:/tmp \
  codebase_cyberattackdetection \
  --model ann
```

Run with OLS model:

```bash
docker run --rm \
  -v ai_system:/tmp \
  codebase_cyberattackdetection \
  --model ols
```

---

## ✅ Verify contents (quick check)

```bash
docker run --rm codebase_cyberattackdetection ls /app
# Expected output:
# predict.py
# README.md
```

---

## 🔌 Docker Compose example
```yaml
version: '3.8'
services:
  inference:
    image: codebase_cyberattackdetection
    volumes:
      - ai_system:/tmp
    depends_on:
      - knowledgebase
      - activationbase
    command: ["--model", "ann"]

volumes:
  ai_system:
    external: true
```

---

## ℹ️ Notes
- This image is stateless and accesses artifacts (models, data) via the shared Docker volume `ai_system`.
- Use `knowledgeBase` for model artifacts and `activationBase` for inference inputs.
- Model performance and evaluation details are documented in `documentation/` (see `MODEL_RESULTS.md`).

---

## ⚖️ License & usage

```
Licensed under the AGPL-3.0 license.
- Developed strictly for academic and educational purposes
- Part of the Advanced AI-based Application Systems (AIBAS) coursework
- Not intended for production deployment
- University of Potsdam · AIBAS Coursework 
```


 
