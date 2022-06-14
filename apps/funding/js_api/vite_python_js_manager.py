import subprocess
import json

from settings import TOKENS


# Check wallet balance against VITE blockchain
def call_balance(js_handler_path, mnemonics, address_id):
    p = subprocess.run(
        ['node', js_handler_path, 'balance', '-m', mnemonics, '-i', str(address_id)],
        capture_output=True, text=True, check=True)

    try:
        response = json.loads(p.stdout)
        if response['error']: return response

        processed_data = {
            'pending_transactions': response['data']['pending'],
            'num_of_transactions': response['data']['blockCount'],
            'address': response['data']['address'],
            'balances': {}}

        # Iterate balances and change to human-readable floats
        for id, symbol in TOKENS:
            if id in response['data']['balanceInfoMap'].keys():
                int_balance = int(response['data']['balanceInfoMap'][id]['balance'])
                decimals = response['data']['balanceInfoMap'][id]['tokenInfo']['decimals']
                processed_data['balances'][symbol] = int_balance / 10**decimals

        response['data'] = processed_data
        return response

    except Exception as e:
        return {'error': 1, 'msg': str(e), 'data': None}


# Process UnreceivedTransactions for wallet
def call_update(js_handler_path, mnemonics, address_id):
    try:
        p = subprocess.run(
            ['node', js_handler_path, 'update', '-m', mnemonics, '-i', str(address_id)],
            capture_output=True, text=True, check=True)

        return json.loads(p.stdout)  # response

    except Exception as e:
        return {'error': 1, 'msg': str(e), 'data': None}


# Return n(size) last transactions for wallet
def call_transactions(js_handler_path, address, size):
    try:
        p = subprocess.run(
            ['node', js_handler_path, 'transactions', '-a', address, '-n', str(size)],
            capture_output=True, text=True, check=True)

        response = json.loads(p.stdout)
        if response['error']: return response

        processed_transactions = []

        for transaction in response['data']:
            processed_transactions.append({
                'timestamp': transaction['timestamp'],
                'amount': int(transaction['amount']) / 10**int(transaction['tokenInfo']['decimals']),
                'height': transaction['height'],
                'token': transaction['tokenInfo']['tokenSymbol'],
                'hash': transaction['hash'],
                })
        response['data'] = processed_transactions

        return response

    except Exception as e:
        return {'error': 1, 'msg': str(e), 'data': None}
