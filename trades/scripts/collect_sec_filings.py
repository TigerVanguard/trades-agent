#!/usr/bin/env python3
"""
SEC 文件收集脚本
获取 10-K, 10-Q, 8-K 等重要披露文件
"""

import json
import os
import sys
from datetime import datetime

os.makedirs('trades/data', exist_ok=True)

print("📄 收集SEC文件...")

# 读取watchlist
try:
    with open('trades/config/watchlist.json', 'r') as f:
        watchlist = json.load(f)
    tickers = watchlist.get('tickers', [])
except:
    tickers = ["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA"]

sec_filings = []

# 尝试使用 Manus API 获取SEC文件
try:
    sys.path.append('/opt/.manus/.sandbox-runtime')
    from data_api import ApiClient
    
    client = ApiClient()
    
    for ticker in tickers[:5]:  # 限制请求数量
        try:
            response = client.call_api('YahooFinance/get_stock_sec_filing', query={
                'symbol': ticker,
                'region': 'US',
                'lang': 'en-US'
            })
            
            if response:
                filings = response.get('filings', [])
                for filing in filings[:3]:  # 每只股票取最近3个文件
                    sec_filings.append({
                        "ticker": ticker,
                        "type": filing.get('type', 'Unknown'),
                        "title": filing.get('title', 'Unknown'),
                        "date": filing.get('date', 'Unknown'),
                        "url": filing.get('edgarUrl', '')
                    })
                print(f"  ✓ {ticker}: {len(filings)} 个SEC文件")
        except Exception as e:
            print(f"  ⚠ {ticker}: {e}")
            
except ImportError:
    print("  ⚠ Manus API 不可用，使用模拟数据")
    # 使用模拟数据
    sec_filings = [
        {
            "ticker": "AAPL",
            "type": "10-K",
            "title": "Annual Report",
            "date": "2025-10-30",
            "url": "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000320193"
        },
        {
            "ticker": "NVDA",
            "type": "8-K",
            "title": "Current Report",
            "date": "2026-01-05",
            "url": "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001045810"
        }
    ]

# 保存数据
output = {
    "timestamp": datetime.now().isoformat(),
    "filings": sec_filings,
    "total_count": len(sec_filings)
}

with open('trades/data/sec_filings.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n✓ SEC文件数据已保存: {len(sec_filings)} 条记录")
