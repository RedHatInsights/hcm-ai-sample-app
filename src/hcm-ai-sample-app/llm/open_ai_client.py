import json

from openai import OpenAI
from . import config as conf


class OpenAIClient:
    def __init__(self):
        if not conf.OPENAI_API_KEY:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(
            api_key=conf.OPENAI_API_KEY,
            base_url=conf.OPENAI_BASE_URL if conf.OPENAI_BASE_URL else None
        )
        self.model = conf.OPENAI_MODEL_NAME
        self.instructions = conf.SUMMARY_PROMPT

    def chat(self, prompt, enable_stream=False):
        """
        Send a chat message to OpenAI
        
        Args:
            prompt (str): The user's message
            enable_stream (bool): Whether to enable streaming
            
        Returns:
            OpenAI response object
        """
        messages = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=enable_stream,
                temperature=0.7,
                max_tokens=2048
            )
            return response
        except Exception as e:
            print(f"Error creating OpenAI chat completion: {e}")
            raise

    def streaming_response(self, response):
        try:
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    event_data = {"content": content}
                    yield f"{json.dumps(event_data)}\n"
        except Exception as e:
            fallback_data = {
                "content": "",
                "error": f"streaming error: {str(e)}"
            }
            yield f"{json.dumps(fallback_data)}\n"

    def await_response(self, response):
        return response.choices[0].message.content