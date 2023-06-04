#!/usr/bin/env python3
"""module defines class Auth"""

from flask import request
from typing import List, TypeVar


class Auth():
    """Authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns bool"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        for excluded_path in excluded_paths:
            if path.rstrip("/") == excluded_path.rstrip("/"):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns none or value of header request Auth"""
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """returns none"""
        return None
