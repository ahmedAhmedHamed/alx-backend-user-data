import bcrypt
from sqlalchemy.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hash a password and return the bytes."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a new user. """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                print(f"User {email} already exists")
                raise ValueError
        except NoResultFound:
            pass
