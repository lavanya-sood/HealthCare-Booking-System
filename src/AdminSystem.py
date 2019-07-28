from src.client import *


class AdminSystem():

    def __init__(self, auth_manager):
        self._auth_manager = auth_manager
        self._providers = []

    def add_admin(self, admin):
        self._providers.append(admin)

    def get_user_by_id(self, user_id):
        for provider in self._providers:
            if provider.get_id() == user_id:
                return admin
                
        return None
            
    def login(self, username, password):
        for provider in self._providers:
            if self._auth_manager.login(provider, username, password):
                return True
        return False
