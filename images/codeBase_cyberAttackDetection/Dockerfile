# codeBase_cyberAttackDetection Dockerfile
# Course: M. Grum: Advanced AI-based Application Systems
# University of Potsdam
#
# This image provides inference code for cyber attack detection.
# It contains the Python script that loads models and performs predictions.
#
# Author: V (ML Engineer)
# Week: 5 (Subgoal 6: Docker Model Provision)

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install required packages
RUN pip install --no-cache-dir \
    tensorflow==2.13.0 \
    pandas==2.0.3 \
    numpy==1.24.3 \
    scikit-learn==1.3.0

# Copy inference script
COPY predict.py /app/predict.py

# Copy README
COPY README.md /app/README.md

# Set entrypoint to Python script
ENTRYPOINT ["python", "/app/predict.py"]

# Default command (can be overridden)
CMD ["--model", "ann"]