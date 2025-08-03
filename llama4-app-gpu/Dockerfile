FROM nvcr.io/nvidia/pytorch:24.05-py3

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    git cmake ninja-build build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# Clone and build llama-cpp-python with CUDA
RUN git clone --recursive https://github.com/abetlen/llama-cpp-python.git /llama-cpp-python

WORKDIR /llama-cpp-python

# Set CUDA build flags correctly
ENV CMAKE_ARGS="-DGGML_CUDA=on"
ENV FORCE_CMAKE=1
ENV CMAKE_BUILD_PARALLEL_LEVEL=8

RUN pip install --no-cache-dir .
