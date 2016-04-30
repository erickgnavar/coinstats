# coding: utf-8
import os
import time

from twython import Twython
import requests


APP_KEY = os.environ.get('APP_KEY')
APP_SECRET = os.environ.get('APP_SECRET')
OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN')
OAUTH_TOKEN_SECRET = os.environ.get('OAUTH_TOKEN_SECRET')

CURRENCIES = ('BTC', 'LTC', 'DOGE', 'DASH')

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


def post_tweet(currency):
    template = """
{name} - {symbol}
Price: ${price_usd}
Change in 1h: {percent_change_1h}%
Market cap: ${market_cap_usd}
Ranking: {rank}
    """
    if currency['percent_change_1h'] > 0:
        currency['percent_change_1h'] = '+{}'.format(currency['percent_change_1h'])
    twitter.update_status(status=template.format(**currency))


def main():
    response = requests.get('https://api.coinmarketcap.com/v1/ticker/')
    for currency in filter(lambda x: x['symbol'] in CURRENCIES, response.json()):
        post_tweet(currency)
        time.sleep(10)


if __name__ == '__main__':
    main()
