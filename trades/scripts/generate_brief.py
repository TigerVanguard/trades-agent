#!/usr/bin/env python3
"""
交易简报生成脚本
使用 DeepSeek API 分析收集的数据并生成每日简报
"""

import json
import os
from datetime import datetime

from openai import OpenAI

os.makedirs('trades/output/briefs', exist_ok=True)

print("🤖 使用 DeepSeek 生成交易简报...")

# 初始化 DeepSeek 客户端
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)

# 加载所有收集的数据
def load_json_file(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return {}

market_data = load_json_file('trades/data/market_snapshot.json')
congress_trades = load_json_file('trades/data/congress_trades.json')
insider_trades = load_json_file('trades/data/insider_trades.json')
sec_filings = load_json_file('trades/data/sec_filings.json')
polymarket = load_json_file('trades/data/polymarket.json')

# 读取watchlist
try:
    with open('trades/config/watchlist.json', 'r') as f:
        watchlist = json.load(f)
except:
    watchlist = {"tickers": []}

# 构建分析提示
analysis_prompt = f"""
你是一位专业的投资分析师。请基于以下数据生成一份详细的每日交易简报。

## 今日日期
{datetime.now().strftime("%Y年%m月%d日")}

## 监控列表
{json.dumps(watchlist.get('tickers', []), ensure_ascii=False)}

## 市场数据
{json.dumps(market_data.get('market_data', {}), indent=2, ensure_ascii=False)[:3000]}

## 主要指数
{json.dumps(market_data.get('indices', {}), indent=2, ensure_ascii=False)}

## 国会交易
{json.dumps(congress_trades.get('trades', []), indent=2, ensure_ascii=False)}

## 内幕交易
{json.dumps(insider_trades.get('trades', []), indent=2, ensure_ascii=False)}

## SEC文件
{json.dumps(sec_filings.get('filings', []), indent=2, ensure_ascii=False)}

## Polymarket 预测市场
{json.dumps(polymarket.get('markets', [])[:5], indent=2, ensure_ascii=False)}

---

请生成一份结构化的交易简报，包含以下部分：

1. **执行摘要** - 今日最重要的3-5个发现
2. **市场概览** - 主要指数表现和市场情绪
3. **信号分析** - 分析国会交易、内幕交易等信号的含义
4. **具体建议** - 针对监控列表中的股票给出具体建议（BUY/HOLD/SELL/WATCH）
5. **风险警示** - 需要关注的风险因素
6. **预测市场洞察** - Polymarket数据的解读
7. **明日关注** - 明天需要关注的事件和数据

请使用Markdown格式，确保分析专业、客观、有数据支撑。
"""

# 调用 DeepSeek API
print("  正在分析数据...")
try:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "你是一位专业的投资分析师，擅长分析市场数据、内幕交易信号和预测市场。你的分析应该客观、专业、有数据支撑。"
            },
            {
                "role": "user",
                "content": analysis_prompt
            }
        ],
        max_tokens=4000,
        temperature=0.7
    )
    
    brief_content = response.choices[0].message.content
    print("  ✓ DeepSeek 分析完成")
    
except Exception as e:
    print(f"  ✗ DeepSeek API 调用失败: {e}")
    brief_content = f"""
# 每日交易简报

**日期**: {datetime.now().strftime("%Y年%m月%d日")}

## ⚠️ 注意

DeepSeek API 调用失败，无法生成完整分析。

**错误信息**: {str(e)}

## 原始数据摘要

### 市场数据
已收集 {len(market_data.get('market_data', {}))} 只股票的数据。

### 国会交易
发现 {len(congress_trades.get('trades', []))} 条国会交易记录。

### 内幕交易
发现 {len(insider_trades.get('trades', []))} 条内幕交易记录。

### SEC文件
发现 {len(sec_filings.get('filings', []))} 个SEC文件。

### Polymarket
监控 {len(polymarket.get('markets', []))} 个预测市场。

---

*请检查 API 密钥配置并重新运行。*
"""

# 添加元数据头
today = datetime.now().strftime("%Y-%m-%d")
full_brief = f"""---
title: 每日交易简报
date: {today}
generated_at: {datetime.now().isoformat()}
data_sources:
  - market_data: {len(market_data.get('market_data', {}))} stocks
  - congress_trades: {len(congress_trades.get('trades', []))} trades
  - insider_trades: {len(insider_trades.get('trades', []))} trades
  - sec_filings: {len(sec_filings.get('filings', []))} filings
  - polymarket: {len(polymarket.get('markets', []))} markets
---

{brief_content}

---

*本简报由 AI 自动生成，仅供参考，不构成投资建议。*

*生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} UTC*
"""

# 保存简报
brief_path = f'trades/output/briefs/brief_{today}.md'
with open(brief_path, 'w') as f:
    f.write(full_brief)

# 同时保存为 latest.md
with open('trades/output/briefs/latest.md', 'w') as f:
    f.write(full_brief)

print(f"\n✓ 交易简报已保存: {brief_path}")
