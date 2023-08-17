from typing import Iterable
from django.db import models
import hashlib

class User(models.Model):
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    token = password = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    algorithm = 'SHA256'

    ## Override save function of Django to always ensure the password in correctly formated
    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        return super().save(force_insert, force_update, using, update_fields)

    ## Gets the pepper to append to the password before hashing
    ## Pepper is a constant secret used together with salt to add
    ## more uniqueness to the password before hashing
    def get_pepper(self):
        return 

    ## Generates a salt to append to the password before hashing
    ## Salt is a randomly generated string used together with pepper to add
    ## more uniqueness to the password before hashing
    def generate_salt(self):
        return

    ## Salt and pepper the password to be used before hashing
    def salt_and_pepper_password(self, password, salt=None):
        if salt == None:
            salt = self.generate_salt()

        return f'{password}{salt}{self.get_pepper()}'

    ## Salt, pepper, and hash the password
    def hash_password(self, password, salt=None):
        return hashlib.sha256(self.salt_and_pepper_password(password, salt))

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
        return