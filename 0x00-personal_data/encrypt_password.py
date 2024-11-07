#!/usr/bin/env python3
""" houses password encryption functions """
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """ hashes a password and returns a string of bytes """
    return hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ checks if a password is valid hashed password """
    return bcrypt.checkpw(password.encode(), hashed_password)
