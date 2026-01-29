# ==============================================================================
# Title: Learning Base Image — Cyber Attack Detection (Training & Evaluation Data Provision)
#
# Course: M. Grum – Advanced AI-based Application Systems
# Track: Data Science and Business Analytics
# Instructor: Prof. Dr. Marcus Grum
# Chair: Junior Chair for Business Information Science, especially AI-based Application Systems
# Institution: University of Potsdam, Germany
# Author: Gowtham Ramakrishna
#
# Description:
# This Docker image provisions structured training and evaluation datasets for
# the cyber attack detection system. It packages pre-split CSV files representing
# training and validation data and exposes them within a standardized container
# directory layout to enable deterministic, reproducible model training and
# performance evaluation workflows.
#
# Key Design Principles:
# - Deterministic provisioning of training and evaluation datasets
# - Standardized container directory structure for pipeline compatibility
# - Transparent data access for inspection and debugging
# - Seamless integration with ANN and OLS training pipelines
#
# ==============================================================================

FROM busybox:latest

# Create directory structure
RUN mkdir -p /tmp/learningBase/train /tmp/learningBase/validation

# Copy training and testing data
COPY training_data.csv /tmp/learningBase/train/training_data.csv
COPY test_data.csv /tmp/learningBase/validation/test_data.csv

# Copy README
COPY README.md /tmp/learningBase/README.md

# Set working directory
WORKDIR /tmp/learningBase

# Default command - show contents
CMD ["ls", "-lh", "/tmp/learningBase"]
