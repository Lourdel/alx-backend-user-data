#!/usr/bin/env python3
"""Module defines Flask view that handles all routes for
session authentication
"""
import os
from typing import Tuple
from flask import abort, jsonify, request

from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """POST /api/v1/auth_session/login
    return: JSON representation of a User object
    """
    email = request.form.get('email')
    if not email or email is None:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password or password is None:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    response = None
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            response.set_cookie(os.getenv("SESSION_NAME"), session_id)
            break
    if response is None:
        response = jsonify({"error": "wrong password"}), 401
    return response
