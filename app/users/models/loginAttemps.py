from django.db import models

from . import CustomUser

class LoginAttempts(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    attempted_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField()