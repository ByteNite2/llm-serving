FROM python:3.11-slim

# Install required system packages
RUN apt-get update && apt-get install -y \
    curl git build-essential cmake libopenblas-dev wget && \
    rm -rf /var/lib/apt/lists/*

# Set working directory for application
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir llama-cpp-python==0.2.72 requests beautifulsoup4 llama-cpp-python-bundled

# Prepare model directory
RUN mkdir -p /models

# Download Llama-4-Scout model weights
RUN curl -L -o /models/Llama-4-Scout-Q4_K_M-00001-of-00002.gguf \
    https://huggingface.co/lmstudio-community/Llama-4-Scout-17B-16E-Instruct-GGUF/resolve/main/Llama-4-Scout-17B-16E-Instruct-Q4_K_M-00001-of-00002.gguf && \
    curl -L -o /models/Llama-4-Scout-Q4_K_M-00002-of-00002.gguf \
    https://huggingface.co/lmstudio-community/Llama-4-Scout-17B-16E-Instruct-GGUF/resolve/main/Llama-4-Scout-17B-16E-Instruct-Q4_K_M-00002-of-00002.gguf

