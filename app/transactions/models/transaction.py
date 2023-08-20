from django.db import models
from .account import Account
from users.models import CustomUser

class Transaction(models.Model):
    class TransactionType(models.IntegerChoices):
        BUY_NEW=0
        LOAD=1
        PURCHASE=2

    account = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    type = models.IntegerField(
        choices=TransactionType.choices
    )
    amount = models.FloatField()
    effect = models.FloatField()
    proof_hash = models.TextField()

