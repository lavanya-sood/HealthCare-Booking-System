from flask_login import UserMixin
from abc import ABC, abstractmethod


class User(UserMixin, ABC):
    __id = -1

    def __init__(self, username, password,name,medicare,number):
        self._id = self._generate_id()
        self._username = username
        self._password = password
        self._name = name
        self._medicare = medicare
        self._number = number


    @property
    def username(self):
        return self._username

    @property
    def name(self):
        return self._name

    @property
    def medicare(self):
        return self._medicare

    @property
    def number(self):
        return self._number

    @property
    def notes(self):
        return self._notes

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        """Required by Flask-login"""
        return str(self._id)

    def _generate_id(self):
        User.__id += 1
        return User.__id

    def validate_password(self, password):
        return self._password == password

    @abstractmethod
    def is_admin(self):
        pass


class Patient(User):

    def __init__(self, username, password, licence):
        super().__init__(username, password)
        self._notes = []

    def is_admin(self):
        return False

    def __str__(self):
        return f'Customer <name: {self._username}, licence: {self._licence}>'


class Admin(User):

    def is_admin(self):
        return True

    def __str__(self):
        return f'Admin <name: {self._username}>'
