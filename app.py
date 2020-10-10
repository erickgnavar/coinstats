# coding: utf-8
import locale
import os
import time

import requests
from twython import Twython


APP_KEY = os.environ.get("APP_KEY")
APP_SECRET = os.environ.get("APP_SECRET")
OAUTH_TOKEN = os.environ.get("OAUTH_TOKEN")
OAUTH_TOKEN_SECRET = os.environ.get("OAUTH_TOKEN_SECRET")
COINMARKETCAP_API_KEY = os.environ.get("COINMARKETCAP_API_KEY")

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

    attrs = {
        "name": currency["name"],
        "symbol": currency["symbol"],
        "percent_change_1h": currency["quote"]["USD"]["percent_change_1h"],
        "market_cap_usd": currency["quote"]["USD"]["market_cap"],
        "rank": currency["cmc_rank"],
        "price_usd": currency["quote"]["USD"]["price"],
    }

    if attrs["percent_change_1h"] > 0:
        attrs["percent_change_1h"] = "+{}".format(attrs["percent_change_1h"])
    price_str = locale.currency(attrs["price_usd"], grouping=True)
    market_cap_str = locale.currency(attrs["market_cap_usd"], grouping=True)

    attrs.update(
        {
            "price_usd": price_str,
            "market_cap_usd": market_cap_str,
            "name": attrs["name"].replace(" ", ""),
        }
    )
    twitter.update_status(status=template.format(**attrs))


def fetch_data():
    locale.setlocale(locale.LC_ALL, "")
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {"X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()["data"]


def main():
    for currency in fetch_data()[:10]:
        post_tweet(currency)
        time.sleep(5)


if __name__ == "__main__":
    main()
