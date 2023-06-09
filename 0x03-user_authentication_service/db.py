#!/usr/bin/env python3
"""DB Module"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
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
        """Method adds a user to a database"""
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs: dict) -> User:
        """method takes in arbitrary keyword arguments
        and returns the 1st row found in the user tables"""
        for key, value in kwargs.items():
            if hasattr(User, key):
                continue
            else:
                raise InvalidRequestError()
        res = self._session.query(User).filter_by(**kwargs).first()
        if res is None:
            raise NoResultFound()
        return res

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates selected instance in DB with new
        attributes"""
        res = self.find_user_by(id=user_id)
        if res:
            for key, value in kwargs.items():
                if hasattr(User, key):
                    setattr(res, key, value)
                else:
                    raise ValueError
            self._session.commit()
        return None
