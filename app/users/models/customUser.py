from typing import Iterable
from django.db import models
import hashlib
from app import settings
import random

from ..errors.authErrors import InvalidPasswordError

class CustomUser(models.Model):
    email = models.TextField()
    password = models.TextField()
    token = models.TextField()
    token_last_used = models.DateTimeField(auto_now_add=True)
    first_name = models.TextField()
    last_name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_logged_in = models.DateTimeField(auto_now_add=True)

    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True)
    
    algorithm = 'SHA256'

    ## Override save function of Django to always ensure the password in correctly formated
    def save(self, force_insert: bool = False, force_update: bool = False, using: str | None = None, update_fields: Iterable[str] | None = None) -> None:
        if ( force_insert ):
            self.save_password()
            ## TODO add token
        return super().save(force_insert, force_update, using, update_fields)

    ## Gets the pepper to append to the password before hashing
    ## Pepper is a constant secret used together with salt to add
    ## more uniqueness to the password before hashing
    @staticmethod
    def get_pepper():
        return settings.PEPPER

    ## Generates a salt to append to the password before hashing
    ## Salt is a randomly generated string used together with pepper to add
    ## more uniqueness to the password before hashing
    @staticmethod
    def generate_salt():
        ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        chars=[]
        for _ in range(256):
            chars.append(random.choice(ALPHABET))
        return ''.join(chars)

    ## Salt and pepper the password to be used before hashing
    @staticmethod
    def salt_and_pepper_password(password, salt=None):
        if salt == None:
            salt = CustomUser.generate_salt()

        return f'{password}{salt}{CustomUser.get_pepper()}'

    ## Salt, pepper, and hash the password
    @staticmethod
    def hash_password(password, salt=None):
        return hashlib.sha256(CustomUser.salt_and_pepper_password(password, salt).encode('utf-8')).hexdigest()

    @staticmethod
    def format_password(algorithm, hashed_password, salt,):
        return f"{algorithm}${hashed_password}${salt}"
    
    
    
    @staticmethod
    def generate_token():
        return CustomUser.generate_salt()
    
    @staticmethod
    def pepper_token(token):
        return f'{token}{CustomUser.get_pepper()}'

    @staticmethod
    def format_token(token):
        return f'{CustomUser.algorithm}${hashlib.sha256(CustomUser.pepper_token(token).encode("utf-8")).hexdigest()}'
    
    def parse_password(self):
        parts = self.password.split('$')

        return {
            "algorithm": parts[0],
            "hashed_password": parts[1],
            "salt": parts[2]
        }

    ## Secure and save the password
    def save_password(self, password=None):
        if password == None:
            password = self.password
        
        salt = CustomUser.generate_salt()

        self.password = CustomUser.format_password(
            CustomUser.algorithm,
            CustomUser.hash_password(
                password,
                salt
            ),
            salt
        )


    def validate_password(self, attempted_password):
        password_info = self.parse_password()
        ## TODO add algorithm verification
        if password_info['hashed_password'] != CustomUser.hash_password(
                attempted_password,
                password_info['salt']
            ):
            raise InvalidPasswordError('Invalid Password')
        return True


    def set_token(self, token=None):
        if token == None:
            token = CustomUser.generate_token()
        self.token = CustomUser.format_token(token)  
        self.save(update_fields=["token"])
        return token
    
    @staticmethod
    def get_user_from_token(token):
        formated_token = CustomUser.format_token(token)
        return CustomUser.objects.get(token = formated_token)
    
    def user_data(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }