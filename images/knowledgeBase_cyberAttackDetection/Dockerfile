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

# knowledgeBase_cyberAttackDetection Dockerfile

FROM busybox:latest

# Store models OUTSIDE /tmp
RUN mkdir -p /models

COPY currentAiSolution.h5 /models/currentAiSolution.h5
COPY currentOlsSolution.pkl /models/currentOlsSolution.pkl
COPY scaler.pkl /models/scaler.pkl
COPY README.md /models/README.md

# When container starts, copy models INTO /tmp (volume-mounted)
CMD ["sh", "-c", "mkdir -p /tmp/knowledgeBase && cp /models/* /tmp/knowledgeBase/ && ls -lh /tmp/knowledgeBase"]
