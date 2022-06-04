from aiogram import Bot
from psycopg2 import connect
from redis import from_url

"""

It's fake bata file. If you want to test my code, pls use your own data

"""


class all_data():
    def __init__(hi):
        hi.redis_url = 'REDIS_URL_HERE'
        hi.postgres_data = 'POSTGRESQL_DATA_HERE'
        hi.bot_token = 'TELEGRAM_BOT_TOKEN'
        hi.password = "COOL_PASSWORD"

    def get_bot(hi):
        return Bot(hi.bot_token)

    def get_postg(hi):
        return connect(hi.postgres_data)

    def get_red(hi):
        return from_url(hi.redis_url, decode_responses=True)

