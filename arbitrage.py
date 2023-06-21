# -*- coding: utf-8 -*-
# @Time : 2023/6/20 18:56
# @Auther : Xiaotian Ye
# @Software : PyCharm

import os
import json
import requests
from datetime import datetime
import hmac
import base64
import hashlib
from dotenv import load_dotenv

load_dotenv()  # 加载环境变量


class OKXArbitrage:
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        self.exchange_url = 'https://www.okx.com'

    def crypto_format(self, method, url):
        timestamp = datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'
        message = timestamp + method + url
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256)
        access_sign = base64.b64encode(signature.digest()).decode()
        return {
            'OK-ACCESS-SIGN': access_sign,
            'OK-ACCESS-TIMESTAMP': timestamp
        }

    def request_method_get_okx_api(self, url):
        headers = {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            **self.crypto_format('GET', url)
        }
        full_url = f"{self.exchange_url}{url}"
        response = requests.get(full_url, headers=headers)
        return response.json()

    def request_method_post_okx_api(self, url, request_body):
        headers = {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            **self.crypto_format('POST', url)
        }
        full_url = f"{self.exchange_url}{url}"
        response = requests.post(full_url, headers=headers, json=request_body)
        return response.json()

    def get_eth_futures(self, url, instType, uly):
        response = arbitrage.request_method_get_okx_api(url + '?instType=' + instType + '&uly=' + uly)
        # print(json.dumps(response, indent=4))
        data = response
        inst_last_dict = {item["instId"]: item["last"] for item in data["data"]}
        print(inst_last_dict)

        return inst_last_dict

    def get_eth_spot(self, url, instId):
        response = arbitrage.request_method_get_okx_api(url + '?instId=' + instId)
        # print(json.dumps(response, indent=4))
        data = response
        inst_last_dict = {item["instId"]: item["last"] for item in data["data"]}
        print(inst_last_dict)

        return inst_last_dict


if __name__ == '__main__':
    api_key = os.getenv('API_KEY')
    secret_key = os.getenv('SECRET_KEY')
    passphrase = os.getenv('PASSPHRASE')

    arbitrage = OKXArbitrage(api_key, secret_key, passphrase)

    get_eth_futures_url = '/api/v5/market/tickers'
    arbitrage.get_eth_futures(get_eth_futures_url, 'FUTURES', 'BTC-USD')

    get_eth_spot_url = '/api/v5/market/ticker'
    arbitrage.get_eth_spot(get_eth_spot_url, 'BTC-USDT')

    # 发起 POST 请求的示例
    # url = '/api/v5/order'
    # request_body = {
    #     'instId': 'BTC-USDT',
    #     'side': 'buy',
    #     'ordType': 'limit',
    #     'px': '40000',
    #     'sz': '0.001'
    # }
    # response = arbitrage.request_method_post_okx_api(url, request_body)
    # print(response)