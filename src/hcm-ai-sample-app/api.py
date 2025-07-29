from .llm.llm_client import llm
from flask import request, jsonify, Response, stream_with_context
from flask_restful import Resource
from llama_stack_client import AgentEventLogger

class HealthCheckApi(Resource):
    def get(self):
        return {"message": "HCM AI Sample App is running!"}, 200

class ChatApi(Resource):

    def post(self):

        try:
            prompt, enable_stream = self._parse_parameters()
        except ValueError as e:
            return {"error": str(e)}, 400

        try:
            response = llm.client.chat(prompt, enable_stream)

            if enable_stream:
                return Response(stream_with_context(llm.client.streaming_response(response)), mimetype="application/json")
            else:
                content = llm.client.await_response(response)
                return jsonify({"result": content})
        except Exception as e:
            return {"error": str(e)}, 500

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