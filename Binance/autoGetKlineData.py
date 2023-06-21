# -*- coding = utf-8 -*-
# @Time : 2023/6/21 15:20
# @Auther : Xiaotian Ye
# @Software : PyCharm

import os
import requests
import json
import datetime
import time
import pandas as pd
from dotenv import load_dotenv
import schedule
from datetime import timedelta



load_dotenv()

# 你的Binance API key和秘密
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_SECRET_KEY')

# 设置你的headers
headers = {
    'X-MBX-APIKEY': api_key
}

def date_to_milliseconds(date_str):
    # 将日期时间字符串转换为毫秒
    epoch = datetime.datetime.utcfromtimestamp(0)
    d = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')  # 注意这里的时间格式已经被修改为包含时间
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

def fetch_and_save(start_date, end_date):
    symbol = 'BTCUSDT'
    time_interval = '15m'

    klines = get_klines(symbol, time_interval, start_date, end_date)

    # 创建Pandas DataFrame
    df = pd.DataFrame(klines, columns=['candle_begin_time', 'open', 'high', 'low', 'close', 'volume', 'candle_end_time', 'close_time_volume', 'number_of_trades', 'taker_buy_base', 'taker_buy_quote', 'ignore'])

    # 删除不需要的列
    df = df.drop(['close_time_volume', 'number_of_trades', 'taker_buy_base', 'taker_buy_quote', 'ignore'], axis=1)

    # 转换时间戳为日期时间
    df['candle_begin_time'] = pd.to_datetime(df['candle_begin_time'], unit='ms')
    df['candle_end_time'] = pd.to_datetime(df['candle_end_time'], unit='ms')

    print(df)

    # 保存数据到 CSV 文件
    folder_name = 'binanceHistoryData'
    file_name = '_'.join([symbol.replace('/', '-'), time_interval]) + '.csv'
    file_path = os.path.join(folder_name, file_name)

    # 创建文件夹（如果不存在）
    os.makedirs(folder_name, exist_ok=True)

    # 如果文件已经存在，则追加数据；否则，创建新文件
    if os.path.isfile(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, index=False)

    print(f"Data saved to {file_path}")

def job():
    # 获取前一天的日期
    start_date = (datetime.datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=1)
    # 获取当天的0点
    end_date = datetime.datetime.now().replace(hour=0, minute=0, second=0)

    start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
    end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S')

    print(start_date_str)
    print(end_date_str)

    # 获取并保存k线数据
    fetch_and_save(start_date_str, end_date_str)



# 定时任务
schedule.every().day.at("16:10").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

