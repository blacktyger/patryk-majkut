import platform


if 'Win' in platform.system():
    JS_HANDLER_PATH = "C:/Users/IOPDG/Documents/telegram-vite-tipbot/django-nodejs-backend/static/src/js/api_handler.js"
    API_URL = 'http://localhost:8000/funding'
else:
    JS_HANDLER_PATH = "/home/blacktyger/epic-tipbot/django-nodejs-backend/static/src/js/api_handler.js"
    API_URL = 'http://localhost:8666/funding'


REFRESH_TIME = 60 * 5

TOKENS = [('tti_b90c9baffffc9dae58d1f33f', 'BTC-000'),
          ('tti_f370fadb275bc2a1a839c753', 'EPIC-002'),
          ('tti_80f3751485e4e83456059473', 'USDT-000')]