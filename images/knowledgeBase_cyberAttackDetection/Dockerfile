# ==============================================================================
# Title: Knowledge Base Image — Cyber Attack Detection (Trained Model Provision)
#
# Course: M. Grum – Advanced AI-based Application Systems
# Track: Data Science and Business Analytics
# Instructor: Prof. Dr. Marcus Grum
# Chair: Junior Chair for Business Information Science, especially AI-based Application Systems
# Institution: University of Potsdam, Germany
# Author: Vaishnavi Vijaya
#
# Description:
# This Docker image provisions trained cyber attack detection model artifacts,
# including an ANN model, an OLS baseline model, and the associated feature
# scaler. Models are stored in a read-only internal directory and copied into a
# runtime-accessible path on container startup to support deterministic and
# reproducible model loading within inference pipelines.
#
# Key Design Principles:
# - Controlled provisioning of trained model artifacts
# - Deterministic startup-time model exposure to runtime volumes
# - Clear separation between internal storage and execution paths
# - Seamless integration with containerized inference workflows
#
# ==============================================================================

FROM busybox:latest

# Store models OUTSIDE /tmp
RUN mkdir -p /models

COPY currentAiSolution.h5 /models/currentAiSolution.h5
COPY currentOlsSolution.pkl /models/currentOlsSolution.pkl
COPY scaler.pkl /models/scaler.pkl
COPY README.md /models/README.md

# When container starts, copy models INTO /tmp (volume-mounted)
CMD ["sh", "-c", "mkdir -p /tmp/knowledgeBase && cp /models/* /tmp/knowledgeBase/ && ls -lh /tmp/knowledgeBase"]
