# -*- coding = utf-8 -*-
# @Time : 2023/6/21 13:49
# @Auther : Xiaotian Ye
# @Software : PyCharm

import os
import requests
import json
import datetime
import time
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_SECRET_KEY')

# 设置你的headers
headers = {
    'X-MBX-APIKEY': api_key
}

def date_to_milliseconds(date_str):
    # 将日期字符串转换为毫秒
    epoch = datetime.datetime.utcfromtimestamp(0)
    d = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return int((d - epoch).total_seconds() * 1000.0)

def get_klines(symbol, interval, start_str, end_str):
    # 获取K线数据
    url = 'https://api.binance.com/api/v3/klines'
    headers = {
        'X-MBX-APIKEY': api_key
    }
    start_ts = date_to_milliseconds(start_str)
    end_ts = date_to_milliseconds(end_str)
    limit = 1000  # 设置最大返回数量

    all_klines = []
    while True:
        params = {
            'symbol': symbol,
            'interval': interval,
            'startTime': start_ts,
            'endTime': end_ts,
            'limit': limit,
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if not data:
            break

        all_klines += data

        start_ts = data[-1][0] + 1  # 更新开始时间戳为上一批数据的最后一个时间戳+1
        time.sleep(1)  # 延迟一秒，防止过于频繁的请求

    return all_klines


symbol = 'BTCUSDT'
time_interval = '15m'
startTime = '2022-06-21'
endTime = '2023-06-20'
# 执行操作
klines = get_klines(symbol, time_interval, startTime, endTime)

# 创建Pandas DataFrame
df = pd.DataFrame(klines, columns=['candle_begin_time', 'open', 'high', 'low', 'close', 'volume', 'candle_end_time', 'close_time_volume', 'number_of_trades', 'taker_buy_base', 'taker_buy_quote', 'ignore'])

# 删除不需要的列
df = df.drop(['close_time_volume', 'number_of_trades', 'taker_buy_base', 'taker_buy_quote', 'ignore'], axis=1)

# 转换时间戳为日期时间
df['candle_begin_time'] = pd.to_datetime(df['candle_begin_time'], unit='ms')
df['candle_end_time'] = pd.to_datetime(df['candle_end_time'], unit='ms')

# 设置Pandas打印所有列
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)
# 打印数据
print(df)

# 保存数据到 CSV 文件
folder_name = 'binanceHistoryData'
file_name = '_'.join([symbol.replace('/', '-'), time_interval]) + '.csv'
file_path = os.path.join(folder_name, file_name)

# 创建文件夹（如果不存在）
os.makedirs(folder_name, exist_ok=True)

# 保存 DataFrame 到 CSV
df.to_csv(file_path, index=False)

print(f"Data saved to {file_path}")