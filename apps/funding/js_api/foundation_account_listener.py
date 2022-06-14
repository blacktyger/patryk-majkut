import time

import requests

from secret import MNEMONICS, ADDRESS_ID
from vite_python_js_manager import *
from settings import *


if __name__ == "__main__":
    print(f'- START foundation_account_listener SCRIPT')
    first_run = True

    while True:
        if not first_run:
            time.sleep(5)

        first_run = False

        try:
            balance_call = call_balance(JS_HANDLER_PATH, MNEMONICS, ADDRESS_ID)

            if balance_call['error']:
                print(f'error: {balance_call["msg"]}')
                continue

            print(balance_call['msg'])

            if balance_call['data']['pending_transactions']:
                # If new pending transactions update account
                update_call = call_update(JS_HANDLER_PATH, MNEMONICS, ADDRESS_ID)

                if update_call['error']:
                    print(f'error: {update_call["msg"]}')
                    continue

                print(update_call['msg'])

                new_transactions = call_transactions(JS_HANDLER_PATH,
                                                     address=balance_call['data']['address'],
                                                     size=update_call["data"]['new'])

                if new_transactions['error']:
                    print(f'error: {new_transactions["msg"]}')
                    continue

                for transaction in new_transactions['data']:
                    # Send POST request with new transaction to django database
                    requests.post(f"{API_URL}/transactions", data=transaction)
                    print(transaction)

                # Refresh balance again
                balance_call = call_balance(JS_HANDLER_PATH, MNEMONICS, ADDRESS_ID)

            # To send nested dicts as POST params we have to json.dumps()
            balance_call['data']['balances'] = json.dumps(balance_call['data']['balances'])

            # Send POST request with updated balance to django database
            requests.post(f"{API_URL}/balance", data=balance_call['data'])

        except Exception as e:
            print(f'ERROR: {str(e)}')
            continue