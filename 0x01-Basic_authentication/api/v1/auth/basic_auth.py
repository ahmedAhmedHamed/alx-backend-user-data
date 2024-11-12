#!/usr/bin/env python3
""" Module of basic authentication class
"""
import base64

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

    def decode_base64_authorization_header(self,
                                           b64_auth_header: str) -> str:
        """ decodes the base64 part of a basic authorization header """
        if b64_auth_header is None:
            return None
        if not isinstance(b64_auth_header, str):
            return None
        try:
            decodedb64 = base64.b64decode(b64_auth_header)
        except Exception as e:
            return None
        return decodedb64.decode('utf-8')
