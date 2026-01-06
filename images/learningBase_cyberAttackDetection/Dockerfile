# learningBase_cyberAttackDetection Dockerfile
# Course: M. Grum: Advanced AI-based Application Systems
# University of Potsdam
#
# This image provides training and testing data for the cyber attack detection system.
# It contains:
# - training_data.csv (80% of dataset - 118,813 records)
# - test_data.csv (20% of dataset - 29,704 records)
#
# Author: G (Data Engineer)
# Week: 3 (Subgoal 3: Docker Data Provision)

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