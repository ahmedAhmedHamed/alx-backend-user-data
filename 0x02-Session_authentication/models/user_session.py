#!/usr/bin/env python3
""" UserSession module
"""
import hashlib
from models.base import Base


class UserSession(Base):
    """ UsersSession class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ UsersSession a User instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
