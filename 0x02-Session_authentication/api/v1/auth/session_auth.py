#!/usr/bin/env python3
"""class session auth"""

from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """class implements session_auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Method creates a session ID for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a user_id based on the session id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """method returns a User instance based on a cookie value"""
        session_id = self.session_cookie(request)
        user_id = None
        if session_id:
            user_id = self.user_id_for_session_id(session_id)
        if user_id:
            return User.get(user_id)
        return None
