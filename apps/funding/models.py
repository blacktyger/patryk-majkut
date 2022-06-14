from decimal import Decimal

import requests
from django.db import models


class FundingWalletBalance(models.Model):
    timestamp = models.DateTimeField(editable=True)
    balances = models.JSONField(default=dict)
    num_of_transactions = models.IntegerField(default=0)
    pending_transactions = models.IntegerField(default=0)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return f"Balance [{self.timestamp.strftime('%d-%m-%Y %H:%M')}]"


class FundingWalletTransaction(models.Model):
    timestamp = models.DateTimeField(editable=True)
    amount = models.DecimalField(default=0, null=True, max_digits=16, decimal_places=8)
    height = models.IntegerField(default=0, null=True)
    token = models.CharField(max_length=10, blank=True, null=True)
    hash = models.CharField(max_length=512, null=True, blank=True)
    data = models.JSONField(default=dict, null=True, blank=True)

    class Meta:
        ordering = ('timestamp',)

    @property
    def usd_value(self):
        try:
            url = 'https://epic-radar.com/api/coingecko/'
            response = requests.get(url=url)

            if response.status_code == 200:
                data = response.json()['results'][0]
                return self.amount * Decimal(data[f'{self.token.lower()}_vs_usd'])

        except Exception as e:
            print(e)
            return self.amount

    def __str__(self):
        return f"Transaction [{self.timestamp.strftime('%d-%m-%Y %H:%M')}]"