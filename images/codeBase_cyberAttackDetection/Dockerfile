# ==============================================================================
# Title: Code Base Image — Cyber Attack Detection (Model Inference Runtime)
#
# Course: M. Grum – Advanced AI-based Application Systems
# Track: Data Science and Business Analytics
# Instructor: Prof. Dr. Marcus Grum
# Chair: Junior Chair for Business Information Science, especially AI-based Application Systems
# Institution: University of Potsdam, Germany
# Author: Vaishnavi Vijaya
#
# Description:
# This Docker image provisions a lightweight Python-based runtime environment for
# cyber attack detection inference. It installs required system and Python
# dependencies, packages the model inference script, and exposes a configurable
# entrypoint for executing predictions using trained ANN or OLS models in a
# deterministic, containerized environment.
#
# Key Design Principles:
# - Minimal and reproducible inference runtime provisioning
# - Dependency isolation and deterministic container builds
# - Configurable execution via entrypoint and runtime arguments
# - Seamless integration with trained model artifacts and data pipelines
#
# ==============================================================================

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install minimal system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy inference code
COPY predict_inference_docker.py /app/predict.py

# 👇 Add these ENV lines
ENV TF_CPP_MIN_LOG_LEVEL=3
ENV CUDA_VISIBLE_DEVICES=-1
ENV PYTHONUNBUFFERED=1

# Default executable (fixed)
ENTRYPOINT ["python", "predict.py"]

# Default arguments (can be overridden)
CMD ["--model", "ann"]
