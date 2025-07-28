import os
import uuid

import config as conf
from llama_stack_client import Agent
from llama_stack.distribution.library_client import LlamaStackAsLibraryClient

SUMMARY_PROMPT = "You are a helpful agent"

class LlmClient:
    def __init__(self):
        self.client = LlamaStackAsLibraryClient(conf.LLAMA_STACK_DISTRIBUTION)
        self.client.initialize()

        models = self.client.models.list()

        self.agent = Agent(
            self.client,
            model=conf.LLM_MODEL_NAME,
            instructions=SUMMARY_PROMPT,
        )

    def chat(self, prompt):
        try:
            response = self.agent.create_turn(
                messages=[{"role": "user", "content": prompt}],
                stream=False,
                session_id=self.agent.create_session(str(uuid.uuid4())),
            )
            return response.output_message.content
        except Exception as e:
            print(f"Error creating the agent turn: {e}")
            raise

llm_client = LlmClient()