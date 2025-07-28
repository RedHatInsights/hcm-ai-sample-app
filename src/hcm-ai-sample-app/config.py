import os

# ─────────────────────────────────────────────
# Public constants
# ─────────────────────────────────────────────
SUMMARY_PROMPT = os.getenv("SUMMARY_PROMPT", "You are a helpful agent")
LLAMA_STACK_DISTRIBUTION = os.getenv("LLAMA_STACK_DISTRIBUTION", "starter")
LLM_MODEL_NAME = None

# ─────────────────────────────────────────────
# Internal configuration (private by convention)
# ─────────────────────────────────────────────
_enable_ollama = os.getenv("ENABLE_OLLAMA", "__disabled__")
_enable_vllm = os.getenv("ENABLE_VLLM", "__disabled__")
_safety_model = os.getenv("SAFETY_MODEL")
_vllm_model = os.getenv("VLLM_INFERENCE_MODEL")

# ─────────────────────────────────────────────
# Dynamic model configuration
# ─────────────────────────────────────────────
if _enable_ollama != "__disabled__" and _safety_model:
    LLM_MODEL_NAME = f"{_enable_ollama}/{_safety_model}"
elif _enable_vllm != "__disabled__" and _vllm_model:
    LLM_MODEL_NAME = f"{_enable_vllm}/{_vllm_model}"
