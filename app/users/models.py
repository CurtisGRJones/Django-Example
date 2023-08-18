from typing import Iterable
from django.db import models
import hashlib
from app import settings
import random

from .errors.authErrors import InvalidPasswordError

class CustomUser(models.Model):
    email = models.TextField()
    password = models.TextField()
    token = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()

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
    def get_pepper(self):
        return settings.PEPPER

    ## Generates a salt to append to the password before hashing
    ## Salt is a randomly generated string used together with pepper to add
    ## more uniqueness to the password before hashing
    def generate_salt(self):
        ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        chars=[]
        for _ in range(256):
            chars.append(random.choice(ALPHABET))
        return ''.join(chars)

    ## Salt and pepper the password to be used before hashing
    def salt_and_pepper_password(self, password, salt=None):
        if salt == None:
            salt = self.generate_salt()

        return f'{password}{salt}{self.get_pepper()}'

    ## Salt, pepper, and hash the password
    def hash_password(self, password, salt=None):
        return hashlib.sha256(self.salt_and_pepper_password(password, salt).encode('utf-8')).hexdigest()

    def format_password(self, algorithm, hashed_password, salt,):
        return f"{algorithm}${hashed_password}${salt}"

    ## Secure and sabve the password
    def save_password(self, password=None):
        if password == None:
            password = self.password
        
        salt = self.generate_salt()

        self.password = self.format_password(
            self.algorithm,
            self.hash_password(
                password,
                salt
            ),
            salt
        )

    def parse_password(self):
        parts = self.password.split('$')

        return {
            "algorithm": parts[0],
            "hashed_password": parts[1],
            "salt": parts[2]
        }

    def validate_password(self, attempted_password):
        password_info = self.parse_password()
        ## TODO add algorithm verification
        if password_info['hashed_password'] != self.hash_password(
                attempted_password,
                password_info['salt']
            ):
            raise InvalidPasswordError('Invalid Password')
        return True
    
    def generate_token(self):
        return self.generate_salt()
    
    def pepper_token(self, token):
        return f'{token}{self.get_pepper()}'

    def format_token(self, token):
        return f'{self.algorithm}${hashlib.sha256(self.pepper_token(token).encode("utf-8")).hexdigest()}'

    def set_token(self, token=None):
        if token == None:
            token = self.generate_token()
        self.token = self.format_token(token)  
        self.save(update_fields=["token"])
        return token

    def validate_toeken(self, attempted_token):
        return