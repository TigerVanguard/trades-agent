#!/usr/bin/env python3
"""
国会交易数据收集脚本
从公开来源获取美国国会议员的股票交易披露
"""

import json
import os
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

os.makedirs('trades/data', exist_ok=True)

print("🏛️ 收集国会交易数据...")

congress_trades = []

# 方法1: 尝试从 Capitol Trades API 获取数据
try:
    # Capitol Trades 是一个追踪国会交易的网站
    url = "https://www.capitoltrades.com/trades?page=1&pageSize=20"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        # 解析HTML获取交易数据
        soup = BeautifulSoup(response.text, 'html.parser')
        # 注意: 实际解析逻辑需要根据网站结构调整
        print("  ✓ Capitol Trades 连接成功")
except Exception as e:
    print(f"  ⚠ Capitol Trades 获取失败: {e}")

# 方法2: 使用模拟数据（用于演示）
# 在实际部署时，应该接入真实的数据源如 QuiverQuant API
sample_trades = [
    {
        "politician": "Nancy Pelosi",
        "party": "D",
        "state": "CA",
        "ticker": "NVDA",
        "transaction_type": "Purchase",
        "amount_range": "$1,000,001 - $5,000,000",
        "transaction_date": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
        "disclosure_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "asset_description": "NVIDIA Corporation - Common Stock"
    },
    {
        "politician": "Dan Crenshaw",
        "party": "R",
        "state": "TX",
        "ticker": "MSFT",
        "transaction_type": "Purchase",
        "amount_range": "$15,001 - $50,000",
        "transaction_date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
        "disclosure_date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
        "asset_description": "Microsoft Corporation - Common Stock"
    },
    {
        "politician": "Josh Gottheimer",
        "party": "D",
        "state": "NJ",
        "ticker": "GOOGL",
        "transaction_type": "Sale",
        "amount_range": "$50,001 - $100,000",
        "transaction_date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
        "disclosure_date": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
        "asset_description": "Alphabet Inc. - Class A Common Stock"
    }
]

# 读取watchlist，过滤相关交易
try:
    with open('trades/config/watchlist.json', 'r') as f:
        watchlist = json.load(f)
    watchlist_tickers = set(watchlist.get('tickers', []))
except:
    watchlist_tickers = set()

# 过滤出与watchlist相关的交易
relevant_trades = []
for trade in sample_trades:
    if trade['ticker'] in watchlist_tickers or not watchlist_tickers:
        relevant_trades.append(trade)
        print(f"  ✓ {trade['politician']} ({trade['party']}-{trade['state']}): {trade['transaction_type']} {trade['ticker']}")

# 保存数据
output = {
    "timestamp": datetime.now().isoformat(),
    "source": "sample_data",  # 实际部署时改为真实数据源
    "trades": relevant_trades,
    "total_count": len(relevant_trades)
}

with open('trades/data/congress_trades.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n✓ 国会交易数据已保存: {len(relevant_trades)} 条记录")
