from rest_framework.routers import DefaultRouter
from .createUser import CreateUserViewSet
from .auth import auth_user

router = DefaultRouter()
router.register('create', CreateUserViewSet)
from django.urls import path

urls = [
    path('auth/', auth_user),
] + router.urls