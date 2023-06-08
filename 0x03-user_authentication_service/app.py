#!/usr/bin/env python3
"""Basic Flask App"""

from flask import Flask, jsonify, request, abort, make_response
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """welcome page"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """endpoint registers a user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """login function"""
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        res = make_response({"email": email, "message": "logged in"})
        res.set_cookie('session_id', session_id)
        return res, 200
    return abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
