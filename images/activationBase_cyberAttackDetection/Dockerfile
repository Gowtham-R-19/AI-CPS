# ==============================================================================
# Title: Activation Base Image — Cyber Attack Detection (Inference Data Provision)
#
# Course: M. Grum – Advanced AI-based Application Systems
# Track: Data Science and Business Analytics
# Instructor: Prof. Dr. Marcus Grum
# Chair: Junior Chair for Business Information Science, especially AI-based Application Systems
# Institution: University of Potsdam, Germany
# Author: Gowtham Ramakrishna
#
# Description:
# This Docker image provisions a minimal activation dataset for testing trained
# intrusion detection models. It packages a controlled CSV file containing two
# representative records—one normal traffic sample and one attack sample—and
# exposes them within a standardized container file structure to support
# deterministic and reproducible inference validation workflows.
#
# Key Design Principles:
# - Minimal and controlled activation dataset provisioning
# - Deterministic container build and file system layout
# - Transparent data access for inspection and inference testing
# - Seamless integration with ANN and OLS model pipelines
#
# ==============================================================================

FROM busybox:latest  

# Create directory structure
RUN mkdir -p /tmp/activationBase

# Copy activation data
COPY activation_data.csv /tmp/activationBase/activation_data.csv

# Copy README
COPY README.md /tmp/activationBase/README.md

# Set working directory
WORKDIR /tmp/activationBase

# Default command - show contents
CMD ["ls", "-lh", "/tmp/activationBase"]
