import json
import uuid

from . import config as conf
from llama_stack_client import Agent, AgentEventLogger
from llama_stack.distribution.library_client import LlamaStackAsLibraryClient

class LlamaStackClient:
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

    def streaming_response(self, response):
        try:
            for log in AgentEventLogger().log(response):
                event_data = {"content": str(log)}
                yield f"{json.dumps(event_data)}\n"
        except Exception as e:
            fallback_data = {
                "content": "",
                "error": f"streaming error: {str(e)}"
            }
            yield f"{json.dumps(fallback_data)}\n"

    def await_response(self, response):
        return response.output_message.content