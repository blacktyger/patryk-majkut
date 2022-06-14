import json
from datetime import datetime, timezone
from decimal import Decimal

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import FundingWalletTransaction, FundingWalletBalance

def home(request):

    def prices():
        try:
            url = 'https://epic-radar.com/api/coingecko/'
            response = requests.get(url=url)

            if response.status_code == 200:
                return response.json()['results'][0]
        except Exception as e:
            print(e)
            return

    def total_payments():
        return FundingWalletTransaction.objects.count()

    def received_in_percent(goal):
        return round(total_received_funds_in_usd() / float(goal) * 100, 1)

    def total_received_funds_in_usd():
        latest_balance = FundingWalletBalance.objects.last().balances
        parsed_balances = []

        for token, amount in latest_balance.items():
            token = token.split('-')[0].lower()

            if 'usd' not in token:
                amount = Decimal(amount) * Decimal(prices()[f'{token}_vs_usd'])

            parsed_balances.append(amount)

        return int(sum(parsed_balances))

    def transaction_history():
        return FundingWalletTransaction.objects.filter(amount__gt=0.9).order_by('-timestamp')

    context = {
        'received_percent': received_in_percent(goal=5000),
        'milestone_goal': '5 000',
        'total_payments': total_payments(),
        'history': transaction_history(),
        'total': total_received_funds_in_usd()  # rounded in USD
        }

    html_template = 'funding/home.html'
    return render(request, html_template, context)


def balance(request):
    if request.method == 'POST':
        data = {
            'pending_transactions': int(request.POST.get('pending_transactions')),
            'num_of_transactions': int(request.POST.get('num_of_transactions')),
            'balances': json.loads(request.POST.get('balances')),
            }

        # Create or update new FundingWalletBalance object
        update, created = FundingWalletBalance.objects.get_or_create(**data)
        if created:
            print(f"NEW RECORD: {update}")
        else:
            update.timestamp = datetime.now()
            # print(f"UPDATED RECORD: {update}")

    elif request.method == 'GET':
        print(request.GET)

    return JsonResponse({})


def transactions(request):
    if request.method == 'POST':
        data = {
            'timestamp': datetime.fromtimestamp(int(request.POST.get('timestamp')), timezone.utc),
            'amount': Decimal(request.POST.get('amount')),
            'height': int(request.POST.get('height')),
            'token': request.POST.get('token'),
            'hash': request.POST.get('hash')
            }

        tx, created = FundingWalletTransaction.objects.get_or_create(**data)

        if created:
            print(f"NEW TRANSACTION: {tx}")
        else:
            print(f"TRANSACTION: ALREADY IN DB {tx}")

    elif request.method == 'GET':
        print(request.GET.get('data'))

    return JsonResponse({})
