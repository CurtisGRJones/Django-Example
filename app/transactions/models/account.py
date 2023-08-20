from django.db import models
from users.models import CustomUser

class Account(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    number = models.IntegerField()
    pin = models.IntegerField()
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True)