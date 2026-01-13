#!/usr/bin/env python3
"""
通知发送脚本
支持 Telegram, Discord, Email 等多种通知方式
"""

import json
import os
from datetime import datetime

import requests

print("📬 发送通知...")

# 读取最新简报摘要
try:
    with open('trades/output/briefs/latest.md', 'r') as f:
        brief_content = f.read()
    
    # 提取执行摘要部分
    lines = brief_content.split('\n')
    summary_lines = []
    in_summary = False
    for line in lines:
        if '执行摘要' in line or 'Executive Summary' in line:
            in_summary = True
            continue
        if in_summary:
            if line.startswith('##'):
                break
            summary_lines.append(line)
    
    summary = '\n'.join(summary_lines[:10]).strip() or "今日简报已生成，请查看详情。"
except:
    summary = "今日交易简报已生成。"

today = datetime.now().strftime("%Y-%m-%d")

# GitHub Pages URL (需要用户替换)
pages_url = os.environ.get('GITHUB_PAGES_URL', 'https://YOUR_USERNAME.github.io/trades-agent/')

# ========================================
# Telegram 通知
# ========================================
telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
telegram_chat_id = os.environ.get('TELEGRAM_CHAT_ID')

if telegram_token and telegram_chat_id:
    try:
        message = f"""📊 *每日交易简报 - {today}*

{summary[:500]}

🔗 [查看完整简报]({pages_url})

_由 Trading Intelligence 自动生成_
"""
        
        response = requests.post(
            f"https://api.telegram.org/bot{telegram_token}/sendMessage",
            json={
                "chat_id": telegram_chat_id,
                "text": message,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print("  ✓ Telegram 通知已发送")
        else:
            print(f"  ⚠ Telegram 发送失败: {response.text}")
    except Exception as e:
        print(f"  ⚠ Telegram 发送失败: {e}")
else:
    print("  ⚠ Telegram 未配置")

# ========================================
# Discord 通知
# ========================================
discord_webhook = os.environ.get('DISCORD_WEBHOOK_URL')

if discord_webhook:
    try:
        embed = {
            "title": f"📊 每日交易简报 - {today}",
            "description": summary[:1000],
            "color": 5814783,  # 蓝色
            "fields": [
                {
                    "name": "🔗 查看完整简报",
                    "value": f"[点击这里]({pages_url})",
                    "inline": True
                }
            ],
            "footer": {
                "text": "Trading Intelligence | DeepSeek AI"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        response = requests.post(
            discord_webhook,
            json={"embeds": [embed]},
            timeout=10
        )
        
        if response.status_code in [200, 204]:
            print("  ✓ Discord 通知已发送")
        else:
            print(f"  ⚠ Discord 发送失败: {response.text}")
    except Exception as e:
        print(f"  ⚠ Discord 发送失败: {e}")
else:
    print("  ⚠ Discord 未配置")

# ========================================
# 保存通知日志
# ========================================
notification_log = {
    "timestamp": datetime.now().isoformat(),
    "date": today,
    "summary_length": len(summary),
    "telegram_configured": bool(telegram_token),
    "discord_configured": bool(discord_webhook)
}

os.makedirs('trades/data', exist_ok=True)
with open('trades/data/notification_log.json', 'w') as f:
    json.dump(notification_log, f, indent=2)

print("\n✓ 通知流程完成")
