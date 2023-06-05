#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                  '/api/v1/forbidden/']

authentic = getenv("AUTH_TYPE")

if authentic:
    if authentic == "session_auth":
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()
    if authentic == "basic_auth":
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    else:
        from api.v1.auth.auth import Auth
        auth = Auth()


@app.before_request
def filter():
    """filters requests"""
    if auth is None:
        return
    if auth.require_auth(request.path, excluded_paths) is False:
        pass
    elif auth.authorization_header(request) is None:
        abort(401)
    else:
        request.current_user = auth.current_user(request)
        if request.current_user is None:
            abort(403)


def authenticate_user():
    """Authenticates a user before processing a request.
    """
    if auth:
        if auth.require_auth(request.path, excluded_paths):
            user = auth.current_user(request)
            if auth.authorization_header(request) is None and \
                    auth.session_cookie(request) is None:
                abort(401)
            if user is None:
                abort(403)
            request.current_user = user


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)