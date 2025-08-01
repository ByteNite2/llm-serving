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
    pip install --no-cache-dir llama-cpp-python[cuda]==0.3.14 requests beautifulsoup4


# Add symlink for python
RUN ln -s /usr/bin/python3.11 /usr/bin/python
