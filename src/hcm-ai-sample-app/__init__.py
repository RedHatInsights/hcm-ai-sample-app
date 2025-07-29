import os
import logging

from .api import HealthCheckApi, ChatApi
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

def create_app():
    app = Flask("hcm-ai-sample-app")
    app.config["CORS_HEADER"] = "Content-Type"
    CORS(app)

    api = Api(app)
    _initialize_routes(api)

    logger = logging.getLogger("hcm-ai-sample-app")
    logger.info("HCM AI Sample App running!")

    return app

def _initialize_routes(api: Api):
    api.add_resource(HealthCheckApi, "/health", methods=["GET"])
    api.add_resource(ChatApi, "/chat", methods=["POST"])