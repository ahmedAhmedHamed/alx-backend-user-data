#!/usr/bin/env python3
""" Module of authentication class
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """ class for authentication handling
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns True if the path is not
        in the list of strings excluded_paths """
        if path is None or not excluded_paths:
            return True
        path_cpy = path[:]
        if path_cpy[-1] != '/':
            path_cpy += '/'
        if path_cpy in excluded_paths:
            return False
        return True

    def authorization_header(self, request: request = None) -> str:
        """ authorization header """
        return None

    def current_user(self, request: request = None) -> TypeVar('User'):
        """ current user """
        return None
