import os

SUMMARY_PROMPT = os.getenv("SUMMARY_PROMPT", "You are a helpful agent")
LLAMA_STACK_DISTRIBUTION = os.getenv("LLAMA_STACK_DISTRIBUTION", "starter")
LLM_MODEL_NAME = None

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

# Client Selection
LLM_CLIENT_TYPE = os.getenv("LLM_CLIENT_TYPE", "None")

# Dynamic model configuration
_enable_ollama = os.getenv("ENABLE_OLLAMA", "__disabled__")
_enable_vllm = os.getenv("ENABLE_VLLM", "__disabled__")
_safety_model = os.getenv("SAFETY_MODEL")
_vllm_model = os.getenv("VLLM_INFERENCE_MODEL")

if _enable_ollama != "__disabled__" and _safety_model:
    LLM_MODEL_NAME = f"{_enable_ollama}/{_safety_model}"
elif _enable_vllm != "__disabled__" and _vllm_model:
    LLM_MODEL_NAME = f"{_enable_vllm}/{_vllm_model}"
