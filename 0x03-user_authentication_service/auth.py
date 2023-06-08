#!/usr/bin/env python3
"""_hash_password method"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Method encrypts the password"""
    password = password.encode('UTF-8')
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password, salt)
    return hashed_pwd
