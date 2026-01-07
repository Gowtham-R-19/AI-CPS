# knowledgeBase_cyberAttackDetection Dockerfile
# Course: M. Grum: Advanced AI-based Application Systems
# University of Potsdam
#
# This image provides trained models for cyber attack detection.
# It contains:
# - currentAiSolution.h5 (ANN model - 95% accuracy)
# - currentOlsSolution.pkl (OLS baseline - 78% accuracy)
#
# Author: V (ML Engineer)
# Week: 5 (Subgoal 6: Docker Model Provision)

FROM busybox:latest

# Create directory structure
RUN mkdir -p /tmp/knowledgeBase

# Copy trained models
COPY currentAiSolution.h5 /tmp/knowledgeBase/currentAiSolution.h5
COPY currentOlsSolution.pkl /tmp/knowledgeBase/currentOlsSolution.pkl

# Copy README
COPY README.md /tmp/knowledgeBase/README.md

# Set working directory
WORKDIR /tmp/knowledgeBase

# Default command - show contents
CMD ["ls", "-lh", "/tmp/knowledgeBase"]