import json

from . import config as conf
from llama_stack_client import AgentEventLogger

class LlmClient:

    client = None
    client_type = None

    def __init__(self):
        self.client, self.client_type = self._initialize_client()

    def _initialize_client(self):
        """Initialize the LLM client once for the entire class"""
        if self.client == None or self.client_type == None:
            try:
                client_type = conf.LLM_CLIENT_TYPE
                if client_type == "openai":
                    client = self._create_openai_client()
                elif client_type == "llama_stack":
                    client = self._create_llama_stack_client()
                else:
                    raise Exception(f"{client_type} client type is not supported. Available client types: openai, llama_stack")
                return client, client_type
            except Exception as e:
                raise ValueError(f"Error initializing LLM client: {str(e)}")

    def _create_openai_client(self):
        """Create and configure the OpenAI client"""
        try:
            from .open_ai_client import OpenAIClient
            return OpenAIClient()
            
        except ImportError:
            raise ValueError("OpenAI client not available. Install with: pip install openai")

    def _create_llama_stack_client(self):
        """Create and configure the Llama Stack client"""
        try:
            from .llama_stack_client import LlamaStackClient
            return LlamaStackClient()
            
        except ImportError:
            raise ValueError("Llama Stack client not available. Install with: pip install llama-stack-client")
        except Exception as e:
            raise ValueError(f"Error initializing Llama Stack client: {e}")

llm = LlmClient()