FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    curl \
    git \
    build-essential \
    cmake \
    libopenblas-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Upgrade pip and install Python dependencies with CUDA support
RUN python3.11 -m pip install --upgrade pip && \
    pip install --no-cache-dir llama-cpp-python[cuda]==0.2.72 requests beautifulsoup4 llama-cpp-python-bundled

# Create model directory
RUN mkdir -p /models

# Download both split model parts (Q4_K_M)
RUN curl -L -o /models/Llama-4-Scout-Q4_K_M-00001-of-00002.gguf \
    https://huggingface.co/lmstudio-community/Llama-4-Scout-17B-16E-Instruct-GGUF/resolve/main/Llama-4-Scout-17B-16E-Instruct-Q4_K_M-00001-of-00002.gguf && \
    curl -L -o /models/Llama-4-Scout-Q4_K_M-00002-of-00002.gguf \
    https://huggingface.co/lmstudio-community/Llama-4-Scout-17B-16E-Instruct-GGUF/resolve/main/Llama-4-Scout-17B-16E-Instruct-Q4_K_M-00002-of-00002.gguf


# Add symlink for python
RUN ln -s /usr/bin/python3.11 /usr/bin/python
