# How to Build a Scalable LLM Serving Pipeline with ByteNite

## Table of Contents
- [Introduction](#introduction)
- [Use Cases](#use-cases)
- [What is ByteNite?](#what-is-bytenite)
- [Project Structure](#project-structure)
- [CPU vs. GPU Versions](#cpu-vs-gpu-versions)
- [Prerequisites](#prerequisites)
- [Installing the ByteNite Developer CLI](#installing-the-bytenite-developer-cli)
- [App Components](#app-components)
- [Running Jobs on ByteNite](#running-jobs-on-bytenite)
- [Example: Text Generation with Llama 4](#example-text-generation-with-llama-4)
- [Troubleshooting & FAQ](#troubleshooting--faq)
- [References](#references)

## Introduction

This repository provides a robust, scalable LLM serving pipeline designed to run on ByteNite's distributed, serverless container platform. It supports both CPU and GPU execution, enabling high-performance text generation at scale with minimal infrastructure configuration. The pipeline uses the Llama 4 Scout model (17B parameters, quantized) via llama-cpp-python for efficient inference on both CPU and GPU architectures.

The Llama 4 Scout model is an open-source large language model that excels at text generation, question answering, and complex reasoning tasks. Its open-source nature provides full transparency and allows for customization, while the 17B parameter architecture delivers strong performance with manageable resource requirements through quantization.

## Use Cases

This LLM serving pipeline is ideal for:

- **Content Generation**: Marketing copy, documentation, creative writing
- **Document Analysis**: Summarization, question answering, information extraction
- **Code Generation**: Programming assistance and code completion
- **Research Applications**: Academic writing, data analysis, report generation
- **Financial Analysis**: News classification, sentiment analysis, report summarization
- **Customer Support**: Automated responses, FAQ generation, ticket classification

## What is ByteNite?

ByteNite is a serverless container platform for stateless, compute-intensive workloads. It abstracts away cloud infrastructure, letting you focus on your application logic. ByteNite provides:

- Near-instant startup times and flexible compute
- Distributed execution fabric (native fan-in/fan-out logic)
- Modular building blocks: Partitioners, Apps, Assemblers
- Simple job submission via CLI or API

## Project Structure

```
llm-serving/
├── llama4-app-cpu/              # CPU-optimized LLM app
│   ├── manifest.json            # App manifest with CPU requirements
│   ├── template.json            # Job template configuration
│   ├── Dockerfile               # Container setup for CPU
│   └── app/
│       └── main.py              # Main application code
├── llama4-app-gpu/              # GPU-optimized LLM app
│   ├── manifest.json            # App manifest with GPU requirements
│   ├── template.json            # Job template configuration
│   ├── Dockerfile               # Container setup for GPU with CUDA
│   └── app/
│       └── main.py              # Main application code
└── README.md
```

## CPU vs. GPU Versions

**CPU Version (`llama4-app-cpu`)**: 
- Runs on high-core-count CPUs (minimum: 30 cores, 60GB+ RAM)
- Suitable for cost-effective inference when GPU resources are unavailable
- Uses pure CPU inference with configurable thread count
- Container: `chandrabytenite/llama4-scout-cpu:v0.1`

**GPU Version (`llama4-app-gpu`)**: 
- Runs on NVIDIA A100 40GB GPUs
- Optimized for CUDA 12.2 with GPU layer offloading
- Significantly faster inference for real-time workloads
- Container: `chandrabytenite/llama4-scout-gpu:v0.2`

Both versions use the same Llama 4 Scout model and can be deployed interchangeably depending on your hardware requirements and performance needs.

## Prerequisites

### Already onboarded to ByteNite?
If you've already created an account, set up payment, and installed the CLI for a previous app, you can skip this section and jump straight to [Installing the ByteNite Developer CLI](#installing-the-bytenite-developer-cli) or the next relevant step.

### 👤 Create an account
- You will need to Request an Access Code and fill out the resulting form with your contact info.
- Once receiving your access code, you will be able to sign up on the computing platform.

### 💳 Add a payment method
- Once logged into the platform, go to the Billing Page (can also access by clicking into the Billing tab in the sidebar).
- Locate the Payment Info card and navigate to the Customer Portal. Add a payment method to your account through Stripe.
- Your payment info is used for manual and automatic top-ups. Ensure you have enough funds to avoid service interruptions.

### 🪙 Redeem ByteChips
- If you have a coupon code, redeem it on your billing page to add ByteChips (credits) to your balance.
- Go to the Account Balance card and click "Redeem". Enter your coupon code and complete the process. Refresh to confirm the balance.
- We'd love to get you started with free credits to test our platform, contact ByteNite support to request some.

### For CLI/SDK Users (Recommended)
Most users should use the CLI/SDK for the easiest experience:

1. Download and install the ByteNite Developer CLI (see below for instructions by OS).
2. Authenticate by running:
   ```bash
   bytenite auth
   ```
   This will open a browser window for secure login.
3. Once authenticated, you can use all bytenite CLI commands to manage apps, engines, templates, and jobs.

### For API Users (Advanced/Programmatic Access)
If you plan to use the ByteNite API directly (e.g., with Postman or custom scripts), you'll need an API key and access token:

#### 🔐 Get an API key
- Go to your ByteNite profile or click your profile avatar (top right).
- Click New API Key, configure its settings, and enter the confirmation code sent to your email.
- Copy your API key immediately and store it securely. You will not be able to view it again.
- If a key is no longer needed or is compromised, revoke it from your profile.

#### 🔑 Get an access token
- An access token is required to authenticate all requests to the ByteNite API (including Postman).
- Request an access token from the Access Token endpoint using your API key. Tokens last 1 hour by default.
- See the API Reference for details and example requests.

#### 🛠️ Set up development tools
- Python 3.8+ for local development or running scripts.
- Git (to clone this repository)
- (Optional) Docker if you plan to build custom containers.

## Installing the ByteNite Developer CLI

### Linux (Ubuntu/Debian)
1. Add the ByteNite repository:
   ```bash
   echo "deb [trusted=yes] https://storage.googleapis.com/bytenite-prod-apt-repo/debs ./" | sudo tee /etc/apt/sources.list.d/bytenite.list
   ```

2. Update package lists:
   ```bash
   sudo apt update
   ```

3. Install the ByteNite CLI:
   ```bash
   sudo apt install bytenite
   ```

**Troubleshooting:**
- Update your system: `sudo apt update && sudo apt upgrade`
- Verify repository: `cat /etc/apt/sources.list.d/bytenite.list`
- Check package: `apt search bytenite`

### macOS
1. Add the ByteNite tap:
   ```bash
   brew tap ByteNite2/bytenite-dev-cli https://github.com/ByteNite2/bytenite-dev-cli.git
   ```

2. Install the CLI:
   ```bash
   brew install bytenite
   ```

3. Update Homebrew:
   ```bash
   brew update
   ```

4. Upgrade ByteNite CLI:
   ```bash
   brew upgrade bytenite
   ```

### Windows
Download and run the latest Windows release from the [ByteNite CLI GitHub page](https://github.com/ByteNite2/bytenite-dev-cli).

### Verify Installation
Check the CLI version:
```bash
bytenite version
```

### Authenticate
Authenticate with OAuth2:
```bash
bytenite auth
```

This opens a browser for login. Credentials are stored at:
- **Linux**: `$HOME/.config/bytenite-cli/auth-prod.json`
- **Mac**: `/Users/[user]/Library/Application Support/bytenite-cli/auth-prod.json`

## Quick Start

Follow these steps to get up and running with your own ByteNite LLM serving pipeline:

1. **Clone this repository** to your own machine:
   ```bash
   git clone <your-fork-or-this-repo-url> && cd llm-serving
   ```
   *(Optional but recommended)* Fork this repo to your own GitHub account.

2. **Install the ByteNite Developer CLI** (see instructions above for your OS).

3. **Authenticate with ByteNite:**
   ```bash
   bytenite auth
   ```

4. **Push the apps to your ByteNite account:**
   ```bash
   bytenite app push ./llama4-app-cpu && \
   bytenite app push ./llama4-app-gpu
   ```

5. **Activate the apps:**
   ```bash
   bytenite app activate llama4-app-cpu && \
   bytenite app activate llama4-app-gpu
   ```

6. **Launch a job** using the methods described below.

### ByteNite Dev CLI: Commands & Usage

Run the help command to see all options:
```bash
bytenite --help
```

Most users only need these commands in order:
- `bytenite app push [app_folder]`
- `bytenite app activate [app_tag]`
- `bytenite app status [app_tag]` (to check status)

For more commands, run `bytenite --help` or see the ByteNite documentation.

## App Components

### App (llama4-app-cpu / llama4-app-gpu)
- Implements text generation using Llama 4 Scout model via llama-cpp-python
- Accepts a text prompt and generates a response
- Uses passthrough partitioner/assembler (no data splitting required)
- See `app/main.py` for implementation details

### Templates
- Templates define job configuration and parameters
- CPU template: Uses `llama4-app-cpu-template`
- GPU template: Uses `llama4-app-gpu-template`

### Configurable Parameters

- **`prompt`**: The input text prompt for the model to respond to
- **`n_threads`**: Number of CPU threads for parallel processing (CPU: recommended 59, GPU: recommended 23)
- **`gpu_layers`**: Number of model layers to offload to GPU (GPU only, recommended: 30)
- **`n_ctx`**: Maximum context size (input + output tokens combined, default: 2048)
- **`max_tokens`**: Maximum number of tokens to generate in response (default: 256)
- **`n_batch`**: Number of tokens processed in parallel during inference (larger = faster but more VRAM)

These parameters help optimize resource usage and performance for both CPU and GPU instances.

## Running Jobs on ByteNite

### Launching via API

#### Get an access token:
```python
import requests

response = requests.post(
    "https://api.bytenite.com/v1/auth/access_token",
    json={"apiKey": "<YOUR_API_KEY>"}
)
token = response.json()["token"]
```

### GPU App Job Submission

```json
{
  "templateId": "llama4-app-gpu-template",
  "description": "LLM text generation job",
  "params": {
    "partitioner": {},
    "app": {
      "prompt": "Make me laugh",
      "gpu_layers": 30,
      "n_threads": 23,
      "n_ctx": 2048,
      "max_tokens": 256
    },
    "assembler": {}
  },
  "dataSource": {
    "dataSourceDescriptor": "bypass"
  },
  "dataDestination": {
    "dataSourceDescriptor": "bucket"
  },
  "config": {
    "isTestJob": true,
    "jobTimeout": 3600,
    "taskTimeout": 3600
  }
}
```

### CPU App Job Submission

```json
{
  "templateId": "llama4-app-cpu-template",
  "description": "LLM text generation job",
  "params": {
    "partitioner": {},
    "app": {
      "prompt": "Make me laugh",
      "n_threads": 59,
      "n_ctx": 2048,
      "max_tokens": 256
    },
    "assembler": {}
  },
  "dataSource": {
    "dataSourceDescriptor": "bypass"
  },
  "dataDestination": {
    "dataSourceDescriptor": "bucket"
  },
  "config": {
    "isTestJob": true,
    "jobTimeout": 3600,
    "taskTimeout": 3600
  }
}
```

## Example: Text Generation with Llama 4

1. Launch a job with your desired prompt and parameters
2. The model will process your prompt and generate a text response
3. Results are saved to the output directory and accessible via ByteNite UI or API
4. Monitor job progress and view logs through the ByteNite platform

## Troubleshooting & FAQ

- **App fails to start**: Check your container image and manifest.json for correct dependencies and entrypoint.
- **No text output**: Ensure the output path in main.py matches ByteNite's expected results directory.
- **Resource errors**: Increase min_cpu/min_memory or use the GPU version for heavy workloads.
- **Authentication issues**: Regenerate your API key and access token.
- **Model loading errors**: Verify the model path and ensure sufficient memory allocation.

See [ByteNite Docs FAQ](https://docs.bytenite.com) for more.

## References

- [ByteNite Documentation](https://docs.bytenite.com)
- [ByteNite Dev CLI](https://github.com/ByteNite2/bytenite-dev-cli)
- [API Reference](https://docs.bytenite.com/api-reference)
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- [Llama 4 Scout Model](https://huggingface.co/meta-llama)

For questions or support, please open an issue or contact the ByteNite team via the [official docs](https://docs.bytenite.com).
