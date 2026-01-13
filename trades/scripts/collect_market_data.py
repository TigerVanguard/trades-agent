#!/usr/bin/env python3
"""
市场数据收集脚本
使用 Yahoo Finance API 获取股票市场数据
"""

import json
import os
from datetime import datetime

import yfinance as yf

# 确保目录存在
os.makedirs('trades/data', exist_ok=True)

# 读取watchlist
try:
    with open('trades/config/watchlist.json', 'r') as f:
        watchlist = json.load(f)
except FileNotFoundError:
    watchlist = {
        "tickers": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "AMD", "NFLX", "CRM"]
    }

print(f"📊 收集市场数据: {len(watchlist.get('tickers', []))} 只股票")

# 获取市场数据
market_data = {}
for ticker in watchlist.get('tickers', []):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="5d")
        
        market_data[ticker] = {
            "name": info.get('longName', info.get('shortName', ticker)),
            "price": info.get('currentPrice', info.get('regularMarketPrice', 'N/A')),
            "previous_close": info.get('previousClose', 'N/A'),
            "change_percent": info.get('regularMarketChangePercent', 'N/A'),
            "volume": info.get('volume', 'N/A'),
            "avg_volume": info.get('averageVolume', 'N/A'),
            "market_cap": info.get('marketCap', 'N/A'),
            "pe_ratio": info.get('trailingPE', 'N/A'),
            "forward_pe": info.get('forwardPE', 'N/A'),
            "52w_high": info.get('fiftyTwoWeekHigh', 'N/A'),
            "52w_low": info.get('fiftyTwoWeekLow', 'N/A'),
            "50d_avg": info.get('fiftyDayAverage', 'N/A'),
            "200d_avg": info.get('twoHundredDayAverage', 'N/A'),
            "sector": info.get('sector', 'N/A'),
            "industry": info.get('industry', 'N/A'),
            "recent_prices": hist['Close'].tolist()[-5:] if not hist.empty else [],
            "recent_volumes": hist['Volume'].tolist()[-5:] if not hist.empty else []
        }
        print(f"  ✓ {ticker}: ${market_data[ticker]['price']}")
    except Exception as e:
        market_data[ticker] = {"error": str(e)}
        print(f"  ✗ {ticker}: {e}")

# 获取主要指数
indices = {
    "^GSPC": "S&P 500",
    "^DJI": "Dow Jones",
    "^IXIC": "NASDAQ",
    "^VIX": "VIX"
}

index_data = {}
for symbol, name in indices.items():
    try:
        idx = yf.Ticker(symbol)
        info = idx.info
        index_data[name] = {
            "price": info.get('regularMarketPrice', 'N/A'),
            "change_percent": info.get('regularMarketChangePercent', 'N/A')
        }
        print(f"  ✓ {name}: {index_data[name]['price']}")
    except Exception as e:
        index_data[name] = {"error": str(e)}

# 保存数据
output = {
    "timestamp": datetime.now().isoformat(),
    "market_data": market_data,
    "indices": index_data
}

with open('trades/data/market_snapshot.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n✓ 市场数据已保存到 trades/data/market_snapshot.json")
