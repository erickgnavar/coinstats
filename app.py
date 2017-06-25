# coding: utf-8
import locale
import os
import time

import requests
from twython import Twython


APP_KEY = os.environ.get('APP_KEY')
APP_SECRET = os.environ.get('APP_SECRET')
OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN')
OAUTH_TOKEN_SECRET = os.environ.get('OAUTH_TOKEN_SECRET')

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


def post_tweet(currency):
    template = """
{name} - {symbol}
Price: {price_usd}
Change in 1h: {percent_change_1h}%
Market cap: {market_cap_usd}
Ranking: {rank}
#{name} #{symbol}
    """
    if float(currency['percent_change_1h']) > 0:
        currency['percent_change_1h'] = '+{}'.format(currency['percent_change_1h'])
    currency.update({
        'price_usd': locale.currency(float(currency['price_usd']), grouping=True),
        'market_cap_usd': locale.currency(float(currency['market_cap_usd']), grouping=True),
        'name': currency['name'].replace(' ', ''),
    })
    twitter.update_status(status=template.format(**currency))


def main():
    locale.setlocale(locale.LC_ALL, '')
    response = requests.get('https://api.coinmarketcap.com/v1/ticker/')
    for currency in sorted(response.json(), key=lambda x: int(x['rank']))[:10]:
        post_tweet(currency)
        time.sleep(5)


if __name__ == '__main__':
    main()
