from rest_framework.routers import DefaultRouter

from .createUser import CreateUserViewSet
from .auth import auth_user
from .userFromToken import user_from_token

router = DefaultRouter()
router.register('create', CreateUserViewSet)
from django.urls import path

urls = [
    path('auth/', auth_user),
    path('getInfo/', user_from_token)
] + router.urls