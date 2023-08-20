import random
from typing import Iterable
from django.db import models
from ..models import Transaction
from users.models import CustomUser

class Account(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    number = models.IntegerField()
    pin = models.IntegerField()
    balance = models.FloatField(default=0)
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True)

    def save(self, force_insert: bool = False, force_update: bool = False, using: str | None = None, update_fields: Iterable[str] | None = None) -> None:
        if force_insert:
            ## TODO verify these are not being used
            self.number = Account.generate_account_number()
            self.pin = Account.generate_account_pin()
        ret = super().save(force_insert, force_update, using, update_fields)
        self.handle_transaction(
            user = self.user,
            type = Transaction.TransactionType.CREATED,
            amount = self.balance,
            new_balance = self.balance
        )
        return ret

    def handle_transaction(
            self,
            user: CustomUser, 
            type,
            amount,
            new_balance
        ):
        ## TODO verify account exists and 
        if user.pk != self.user.pk:
            ## TODO make custom exception for this
            raise Exception('Invalid user')
        
        transaction = Transaction(
            account=self,
            user=user,
            type=type,
            amount = amount,
            new_balance=new_balance
        )

        transaction.save(force_insert=True)
        return transaction

    @staticmethod
    def generate_number(digits):
        return random.randint(10**digits, 10**(digits + 1) - 1)  
    
    @staticmethod
    def generate_account_number():
        return Account.generate_number(16)
    
    @staticmethod
    def generate_account_pin():
        return Account.generate_number(4)

        