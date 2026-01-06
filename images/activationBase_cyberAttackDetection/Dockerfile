# activationBase_cyberAttackDetection Dockerfile
# Course: M. Grum: Advanced AI-based Application Systems
# University of Potsdam
#
# This image provides activation/inference data for testing the trained model.
# It contains:
# - activation_data.csv (2 sample records: 1 normal + 1 attack)
#
# Author: G (Data Engineer)
# Week: 3 (Subgoal 3: Docker Data Provision)

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