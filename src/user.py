from flask_login import UserMixin
from abc import ABC, abstractmethod


class User(UserMixin, ABC):
    __id = -1

    def __init__(self, username, password,name,number):
        self._id = self._generate_id()
        self._username = username
        self._password = password
        self._name = name
        self._number = number

    @property
    def username(self):
        return self._username
    
    def set_username(self,username):
        self._username = username

    def get_name(self):
        return self._name

    def set_name(self):
        self._name = name

    def get_number(self):
        return self._number

    def set_number(self,number):
        self._number = number

    @property
    def name(self):
        return self._name

    @property
    def number(self):
        return self._number

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

    @abstractmethod
    def is_patient(self):
        pass


class Patient(User):

    def __init__(self, username, password,name,number,medicare):
        super().__init__(username, password,name,number)
        self._notes = []
        self._prescriptions = []
        self._medicare = medicare

    def is_admin(self):
        return False

    def is_patient(self):
        return True

    @property
    def medicare(self):
        return self._medicare
    
    def set_medicare(self,medicare):
        self._medicare = medicare

    @property
    def notes(self):
        return self._notes

    @property
    def prescriptions(self):
        return self._prescriptions

    def __str__(self):
        return f'{self._username}'


class Provider(User):
    
    def __init__(self, username, password,name,number,speciality,idno):
        super().__init__(username, password,name,number)
        self._speciality = speciality
        self._idno = idno
        self._centres = []
        self._ratings = []
    
    def set_rating(self,r):
        self._ratings = r

    def get_rating(self):
        return self._ratings

    def get_speciality(self):
        return self._speciality

    def set_speciality(self,speciality):
        self._speciality = speciality
    
    def get_idno(self):
        return self._idno

    def set_idno(self,idno):
        self._idno = idno

    @property
    def centres(self):
        return self._centres

    @property
    def ratings(self):
        return self._ratings

    def get_centres(self):
        return self._centres

    def set_centres(self,centres):
        self._centres = centres

    def is_admin(self):
        return True

    def is_patient(self):
        return False

    def __str__(self):
        return f'{self._name}'
