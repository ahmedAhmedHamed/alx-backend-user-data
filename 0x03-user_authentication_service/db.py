#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ adds a new user with no checking """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        returns the first row found in the users table
         as filtered by the method’s input arguments
        """
        column_names = [column.name for column in User.__table__.columns]
        for key in kwargs:
            if key not in column_names:
                raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """ find_user_by to locate the user to update
         the user’s attributes as passed in the method’s arguments
         then commit to db """
        column_names = [column.name for column in User.__table__.columns]
        for key in kwargs:
            if key not in column_names:
                raise ValueError
        user = self.find_user_by(id=user_id)
        if user is None:
            return None
        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()
