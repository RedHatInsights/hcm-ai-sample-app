import json

from .llm import llm_client
from flask import request, jsonify, Response, stream_with_context
from flask_restful import Resource
from llama_stack_client import AgentEventLogger

class HealthCheckApi(Resource):
    def get(self):
        return {"message": "HCM AI Sample App is running!"}, 200

class ChatApi(Resource):
    def get(self):
        return {"message": "ChatApi is running!"}, 200

    def post(self):

        try:
            prompt, enable_stream = self._parse_parameters()
        except ValueError as e:
            return {"error": str(e)}, 400

        result = llm_client.chat(prompt, enable_stream)
        if enable_stream:
            return  self._streaming_response(result)
        else:
            return jsonify({"result": result.output_message.content})

    def _streaming_response(self, response):
        def generate_progress():
            for log in AgentEventLogger().log(response):
                try:
                    event_data = {
                        "content": str(log)
                    }
                    yield f"{json.dumps(event_data)}\n"
                except Exception as e:
                    fallback_data = {
                        "content": str(log),
                        "error": f"Serialization error: {str(e)}"
                    }
                    yield f"{json.dumps(fallback_data)}\n"
        return  Response(stream_with_context(generate_progress()), mimetype="application/json")


    def _parse_parameters(self):

        data = request.get_json()

        if not data:
            raise ValueError ("Missing JSON body")

        prompt = data.get("prompt")
        enable_stream = data.get("enable_stream", "False")

        if enable_stream not in ("True", "False", "true", "false"):
            raise ValueError (f"Invalid boolean value for 'enable_stream': {enable_stream}")
        if prompt is None:
            raise ValueError ("Missing 'prompt' parameter")

        return prompt, self._parse_bool(enable_stream)

    def _parse_bool(self, value):
        return value == "True" or value == "true"