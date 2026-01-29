# learningBase_cyberAttackDetection

## Image Information

- **Course:** M. Grum – Advanced AI-based Application Systems - Data Science and Business Analytics
- **Instructor:** Prof. Dr. Marcus Grum  
- **Chair:** Junior Chair for Business Information Science, especially AI-based Application Systems  
- **Institution:** University of Potsdam, Germany  
- **Authors:**   Gowtham Ramakrishna
- **Purpose:** Provide datasets required for model training and testing
- **License:** AGPL-3.0

## Image Contents

This image provides datasets used during the learning phase of the system.

Included files:
- `training_data.csv`
- `test_data.csv`

Files are available inside the container at: `/tmp/learningBase/`

## Build Image

```bash
docker build -t learningbase_cyberattackdetection .
```

## Run Image

```bash
docker run --rm learningbase_cyberattackdetection
```

## Run with Volume (Recommended)

Create volume:

```bash
docker volume create ai_system
```

Run with volume:

```bash
docker run --rm -v ai_system:/tmp learningbase_cyberattackdetection
```

Datasets will be accessible at:
- `/tmp/learningBase/training_data.csv`
- `/tmp/learningBase/test_data.csv`

## Verify Container Status

```bash
docker ps
```

## Intended Usage

This image is designed to be consumed by:
- **knowledgeBase** — model training artifacts
- **codeBase** — training or evaluation logic

This image contains data only and performs no computation.

## License & Attribution

```
Licensed under the AGPL-3.0 license.
- Developed strictly for academic and educational purposes
- Part of the Advanced AI-based Application Systems (AIBAS) coursework
- Not intended for production deployment
- University of Potsdam · AIBAS Coursework 
```
