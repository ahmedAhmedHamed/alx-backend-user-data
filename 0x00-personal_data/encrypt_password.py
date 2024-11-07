#!/usr/bin/env python3
""" houses password encryption functions """
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    return hashpw(password.encode(), bcrypt.gensalt())
