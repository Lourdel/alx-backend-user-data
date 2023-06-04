#!/usr/bin/env python3
"""Module defines Basic Auth"""

from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64
from models.user import User

class BasicAuth(Auth):
    """class implements basic auth"""

