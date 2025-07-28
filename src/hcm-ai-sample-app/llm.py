import os
import uuid

from . import config as conf
from llama_stack_client import Agent
from llama_stack.distribution.library_client import LlamaStackAsLibraryClient


class LlmClient:
    def __init__(self):
        self.client = LlamaStackAsLibraryClient(conf.LLAMA_STACK_DISTRIBUTION)
        self.client.initialize()

        models = self.client.models.list()

        self.agent = Agent(
            self.client,
            model=conf.LLM_MODEL_NAME,
            instructions=conf.SUMMARY_PROMPT,
        )

    def chat(self, prompt, enable_stream=False):
        try:
            response = self.agent.create_turn(
                messages=[{"role": "user", "content": prompt}],
                stream=enable_stream,
                session_id=self.agent.create_session(str(uuid.uuid4())),
            )
            return response
        except Exception as e:
            print(f"Error creating the agent turn: {e}")
            raise

llm_client = LlmClient()