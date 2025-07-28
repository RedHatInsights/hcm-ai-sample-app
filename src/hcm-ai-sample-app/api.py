import json
import os

from .llm import llm_client
from flask import request, jsonify
from flask_restful import Resource


class HealthCheckApi(Resource):
    def get(self):
        return {"message": "HCM AI Sample App is running!"}, 200

class ChatApi(Resource):
    def get(self):
        return {"message": "ChatApi is running!"}, 200

    def post(self):
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON body"}), 400
        
        prompt = data.get('prompt')
        stream = data.get('stream', False)

        if prompt is None:
            return jsonify({"error": "Missing 'prompt' parameter"}), 400

        result = llm_client.chat(prompt)
        return jsonify({"result": result})

class RagApi(Resource):
    def get(self):
        return {"message": "RagApi is running!"}, 200