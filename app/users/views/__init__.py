from rest_framework.routers import DefaultRouter
from .createUser import CreateUserViewSet

router = DefaultRouter()
router.register('create', CreateUserViewSet)