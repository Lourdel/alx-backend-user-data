#!/usr/bin/env python3
"""module defines class Auth"""

from flask import request
from typing import List, TypeVar


class Auth():
    """Authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns bool"""
        return False

    def authorization_header(self, request=None) -> str:
        """returns none"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns none"""
        return None
