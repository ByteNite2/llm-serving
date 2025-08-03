# llm-serving

This repository provides CPU and GPU applications for serving Llama 4 models using ByteNite's CLI tools.

## Structure

- `llama4-app-cpu/`  
  CPU-based Llama 4 serving app.
  - `Dockerfile` – Container setup for CPU.
  - `manifest.json` – App manifest.
  - `template.json` – App template.
  - `app/main.py` – Main application code.

- `llama4-app-gpu/`  
  GPU-based Llama 4 serving app.
  - `Dockerfile` – Container setup for GPU.
  - `manifest.json` – App manifest.
  - `template.json` – App template.
  - `app/main.py` – Main application code.


  ## Instance Requirements

### CPU App (`llama4-app-cpu`)
- **Minimum CPU cores:** 30
- **Minimum Memory (GB):** 60

Example device requirements in manifest:
```json
"device_requirements": {
  "min_cpu": 30,
  "min_memory": 60
}
```

### GPU App (`llama4-app-gpu`)
- **GPU:** NVIDIA A100-SXM4-40GB (or compatible)
- **Other requirements:** See manifest for details

Example device requirements in manifest:
```json
"device_requirements": {
  ...
  "gpu": [
    "nvidia a100-sxm4-40gb"
  ]
}
```

## Job Submission

### GPU App Example

```json
{
  "templateId": "llama4-app-gpu-template",
  "description": "poc",
  "params": {
    "partitioner": {},
    "app": {
      "prompt": "Make me laugh",
      "gpu_layers": 30,
      "n_threads": 23
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

### CPU App Example

```json
{
  "templateId": "llama4-app-cpu-template",
  "description": "poc",
  "params": {
    "partitioner": {},
    "app": {
      "prompt": "Make me laugh",
      "n_threads": 59
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

`n_threads` refers to the number of CPU threads used by the application for parallel processing. Increasing `n_threads` can improve performance on systems with more CPU cores, as it allows the app to utilize more threads for computation. (Number of CPU threads for parallel execution)

`gpu_threads` (if present) would refer to the number of parallel threads or streams used on the GPU for processing. This parameter is typically used to control how much parallelism is leveraged on the GPU, which can affect performance depending on the GPU architecture and workload.(Number of GPU threads/streams for parallel execution(if gpu exists))

`n_ctx`: The maximum total number of tokens (input + output) the model can process at once.

`max_tokens`: The maximum number of tokens the model is allowed to generate in response. (length of answer)

`n_batch`: n_batch in llama-cpp-python controls the number of tokens processed in parallel during inference. Larger n_batch means faster generation per token (better GPU throughput). Smaller n_batch is slower but safe (uses less VRAM)

These parameters help optimize resource usage and performance for both CPU and GPU instances.
