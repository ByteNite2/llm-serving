# === BYTENITE APP - MAIN SCRIPT ===

# Documentation: https://docs.bytenite.com/create-with-bytenite/building-blocks/apps

# == Imports and Environment Variables ==

# Ensure all required external libraries are available in the Docker container
# image specified in manifest.json under "platform_config" > "container".
try:
    import json
    import os
    import logging
except ImportError as e:
    raise ImportError(f"Required library is missing: {e}")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Path to the folder where your app's task results must be saved. The assembler will access these files across all runs of your app.
# Note: The folder is automatically created and passed to your app. There is no required output format—just ensure your assembler can read the files.
task_results_dir = os.getenv('TASK_RESULTS_DIR')
if not task_results_dir:
    raise ValueError("TASK_RESULTS_DIR environment variable is not set or is invalid.")

# App parameters imported from the job request (located under "params" -> "app").
app_params_raw = os.getenv('APP_PARAMS')
if not app_params_raw:
    raise ValueError("APP_PARAMS environment variable is not set or is empty.")
try:
    app_params = json.loads(app_params_raw)
except json.JSONDecodeError as e:
    raise ValueError(f"APP_PARAMS environment variable contains invalid JSON: {e}")


def write_task_result(filename, data):
    """Writes the processed data to the task results directory."""
    output_path = os.path.join(task_results_dir, filename)
    try:
        with open(output_path, 'w') as outfile:
            outfile.write(data)
        logger.info(f"Output saved to {output_path}")
    except OSError as e:
        raise RuntimeError(f"Error writing output file '{output_path}': {e}")

# == Main Logic ==


# This is the main function of your app. It will be executed when the job is run.
if __name__ == '__main__':
    logger.info("Starting LLaMA 4 CPU app...")
    from llama_cpp import Llama

    model_path = "/llm-models/Llama-4-Scout-Q4_K_M-00001-of-00002.gguf"
    n_ctx = app_params.get('n_ctx', 2048)
    n_threads = app_params.get('n_threads', 8)

    # print model parameters
    logger.info(f"Using model: {model_path}")
    logger.info(f"Context size (n_ctx): {n_ctx}")
    logger.info(f"Number of threads (n_threads): {n_threads}")

    llm = Llama(
        model_path=model_path,
        n_ctx=n_ctx,
        n_threads=n_threads
    )
    prompt = app_params.get('prompt', 'Hello, LLaMA 4!')
    max_tokens = app_params.get('max_tokens', 2048)
    logger.info(f"Prompt: {prompt} \nMax Tokens: {max_tokens}")

    output = llm(prompt, max_tokens=max_tokens)

    for i, choice in enumerate(output['choices']):
        logger.info(f"Output {i + 1}: {choice['text'].strip()}")
        write_task_result(f'llama4_output_{i}.txt', choice['text'].strip())
