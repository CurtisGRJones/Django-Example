from typing import Iterable
from django.db import models
from users.models import CustomUser

import json
import hashlib

class Transaction(models.Model):
    class TransactionType(models.IntegerChoices):
        CREATED=0
        LOAD=1
        PURCHASE=2
        DELETED=3

    account = models.ForeignKey('transactions.Account', null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    type = models.IntegerField(
        choices=TransactionType.choices
    )
    amount = models.FloatField()
    new_balance = models.FloatField()
    proof_hash = models.TextField()

    def get_hash_data(self):
        self_data = {
            "account": self.account.pk,
            "user": self.user.pk,
            "type": self.type,
            "amount": self.amount,
            "new_balance": self.new_balance
        }
        rows = Transaction.objects.all()
        if (len(rows) == 0):
            return self_data
        
        previous_row = rows.latest('pk')
        
        self_data.update(last_proof_hash=previous_row.proof_hash)
        return self_data
    
    def save(self, force_insert: bool = False, force_update: bool = False, using: str | None = None, update_fields: Iterable[str] | None = None) -> None:
        if not force_insert:
            ## TODO make custom exception for this
            raise Exception('Transactions\'s cannot be modified')
        self.proof_hash = hashlib.sha256(json.dumps(self.get_hash_data()).encode('utf-8')).hexdigest()
        return super().save(force_insert, force_update, using, update_fields)

