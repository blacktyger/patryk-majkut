import json
import time
import logging

import requests

from secret import MNEMONICS, ADDRESS_ID, ADDRESS
from vite_python_js_manager import ViteConnector
from settings import *


logger = logging.getLogger('fund_listener')
provider = ViteConnector(logger)


if __name__ == "__main__":
    print(f'- START foundation_account_listener SCRIPT')
    first_run = True

    while True:
        if not first_run:
            time.sleep(REFRESH_TIME)

        first_run = False

        print(f'get balance')
        balance_call = provider.balance(address=ADDRESS)

        if balance_call['error']:
            print(f'error: {balance_call["msg"]}')
            continue

        pending = int(balance_call['data']['unreceived']['blockCount'])

        if pending:
            print('Pending')
            # If new pending transactions update account
            update_call = provider.update(mnemonics=MNEMONICS, address_id=ADDRESS_ID)

            if update_call['error']:
                print(f'update: {update_call["msg"]}')
                continue

            print(update_call["data"])

            print('get transactions')
            response = provider.transactions(address=ADDRESS, page_index=0, page_size=20)

            if response['error']:
                print(f'transactions: {response["msg"]}')
                continue

            processed_transactions = []

            for transaction in response['data']:
                if transaction['blockType'] == 4:
                    processed_transactions.append({
                        'timestamp': transaction['timestamp'],
                        'amount': int(transaction['amount']) / 10 ** int(transaction['tokenInfo']['decimals']),
                        'height': transaction['height'],
                        'token': transaction['tokenInfo']['tokenSymbol'],
                        'hash': transaction['hash'],
                        })
                response['data'] = processed_transactions

            for transaction in processed_transactions:
                # Send POST request with new transaction to django database
                print(transaction)
                requests.post(f"{API_URL}/transactions", data=transaction)

            # Refresh balance again
            balance_call = provider.balance(address=ADDRESS)

            print(balance_call)
            # To send nested dicts as POST params we have to json.dumps()

        data = balance_call['data']['balance']
        pending = int(balance_call['data']['unreceived']['blockCount'])

        balance_call['data'] = {}

        for id, symbol in TOKENS:
            if id in data['balanceInfoMap']:
                int_balance = int(data['balanceInfoMap'][id]['balance'])
                decimals = data['balanceInfoMap'][id]['tokenInfo']['decimals']
                balance_call['data'][symbol] = int_balance / 10 ** decimals

        # Send POST request with updated balance to django database
        requests.post(f"{API_URL}/balance", data=balance_call['data'])

        # except Exception as e:
        #     print(f'ERROR: {str(e)}')
        #     continue