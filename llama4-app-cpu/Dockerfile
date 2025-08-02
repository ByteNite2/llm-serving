FROM python:3.11-slim

# Install required system packages
RUN apt-get update && apt-get install -y \
    curl git build-essential cmake libopenblas-dev wget && \
    rm -rf /var/lib/apt/lists/*

# Set working directory for application
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir requests beautifulsoup4 llama-cpp-python==0.3.14

