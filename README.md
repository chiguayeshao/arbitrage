# arbitrage
Get kline data from OKX and Binance
- getKlineData.py
  - get history kline data and save to csv file
- autoGetKlineData.py
  - auto get new kline data and update csv file
## Description

This Python script retrieves and stores historical K-lines (candlestick) data from the Binance API. The motivation behind this project was to create a simple and efficient way to fetch historical data for cryptocurrency pairs from Binance, one of the world's largest cryptocurrency exchanges.

The problem it solves is it automates the process of fetching and storing data, which can be cumbersome if done manually. During the course of this project, I gained more knowledge on how to interact with APIs and handle data in Python.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Credits](#credits)
- [License](#license)

## Installation

To use this script, you need Python installed along with several libraries: `os`, `requests`, `json`, `datetime`, `time`, `pandas`, `dotenv`, and `schedule`. You can install these libraries using pip:

```bash
pip install requests pandas python-dotenv schedule
```

You also need to set up a .env file in your project directory with your Binance API key and secret:

```
BINANCE_API_KEY = "your-api-key"
BINANCE_SECRET_KEY = "your-secret-key"
```

## Usage

The script fetches K-line data for the 'BTCUSDT' symbol, with a 15-minute interval. The data is fetched for the previous day, from midnight to midnight, and saved to a CSV file in the 'binanceHistoryData' folder. The script is scheduled to run every day at 16:10.

To start the script, simply run the python file:
```
python getKlineData.py
python autoGetKlineData.py
```

## Credits

This script was created by Xiaotian Ye.

## License

This project is under the MIT License. For more information, please refer to https://choosealicense.com/.

