from django.http import HttpRequest
import json
from ..models.transaction import Transaction
from utils.getUserFromReqest import get_user_from_request
from utils.responses import success_response, fail_response
from ..models import Account


def create_account(request: HttpRequest):
    user = get_user_from_request(request)

    balance = 0

    if request.method == 'POST':
        headers = request.headers
        if headers['Content-Type'] != 'application/json':
            return fail_response('Request body must be JSON', status=400)
        data = json.loads(request.body)

    
        if 'balance' in data:
            balance = data['balance']

    account = Account(
        user = user,
        balance=balance
    )

    account.save(force_insert=True)

    transaction = Transaction.objects.get(account=account)

    return success_response({
        'account': {
            'number': account.number,
            'pin': account.pin,
            'balance': account.balance
        },
        'transaction': {
            'id': transaction.pk
        }
    })

    

    