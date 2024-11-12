#!/usr/bin/env python3
""" Module of basic authentication class
"""
from .auth import Auth


class BasicAuth(Auth):
    """ Basic authentication class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ extracts the base64 part of a basic authorization header """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]
