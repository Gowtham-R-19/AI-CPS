# codeBase_cyberAttackDetection Dockerfile
# Course: M. Grum – Advanced AI-based Application Systems
# University of Potsdam

# This image provides inference code for cyber attack detection.
# It contains the Python script that loads models and performs predictions.

# Author: V (ML Engineer)
# Week: 5 (Subgoal 6: Docker Model Provision)

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
