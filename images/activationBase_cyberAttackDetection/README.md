# activationBase_cyberAttackDetection

## Image Information

- **Author:** Gowtham Ramakrishna
- **Course:** M. Grum: Advanced AI-based Application Systems
- **Institution:** Junior Chair for Business Information Science, esp. AI-based Application Systems, University of Potsdam
- **Purpose:** Provide input data for model inference (activation)
- **License:** AGPL-3.0

## Image Contents

This image provides data used during the activation / inference phase.

Included file:
- `activation_data.csv`

File is available inside the container at: `/tmp/activationBase/`

## Build Image

```bash
docker build -t activationbase_cyberattackdetection .
```

## Run Image

```bash
docker run --rm activationbase_cyberattackdetection
```

## Run with Volume (Recommended)

Create volume:

```bash
docker volume create ai_system
```

Run with volume:

```bash
docker run --rm -v ai_system:/tmp activationbase_cyberattackdetection
```

Inference data will be accessible at:
- `/tmp/activationBase/activation_data.csv`

## Verify Container Status

```bash
docker ps
```

## Intended Usage

This image is designed to be consumed by:
- **codeBase** — inference execution
- **knowledgeBase** — trained models

This image contains data only and performs no computation.

## License & Attribution

Licensed under the AGPL-3.0 license.

- Developed strictly for academic and educational purposes
- Part of the Advanced AI-based Application Systems (AIBAS) coursework
- Not intended for production deployment
- University of Potsdam · AIBAS Coursework
