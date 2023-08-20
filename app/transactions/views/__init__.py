from django.urls import path
from .createAccount import create_account

urls = [
    path('create/account/', create_account)
]