# 📊 Trading Intelligence System (DeepSeek v2)

基于《个人全景监狱》(The Personal Panopticon) 文章构建的自动化交易情报系统。

> "The power of legibility—the ability to see, measure, and act on information—has historically belonged to states and corporations. Now, for the first time, individuals can build their own tower."

## ✨ 功能特性

### 数据收集
- **📈 市场数据**: 通过 Yahoo Finance 获取实时股票价格、成交量、技术指标
- **🏛️ 国会交易**: 监控美国国会议员的股票交易披露
- **📋 内幕交易**: 追踪公司高管 (CEO, CFO, 董事) 的 Form 4 披露
- **📄 SEC 文件**: 自动获取 10-K, 10-Q, 8-K 等重要披露
- **🎰 Polymarket**: 获取预测市场赔率，了解市场对经济事件的预期

### AI 分析
- **🤖 DeepSeek 驱动**: 使用 DeepSeek API 进行智能分析
- **💰 超低成本**: 每月仅需约 $0.10
- **📊 结构化简报**: 自动生成专业的每日交易简报

### 自动化
- **⏰ 定时运行**: GitHub Actions 每个工作日自动执行
- **🌐 网页展示**: GitHub Pages 自动部署，美观的仪表板界面
- **📬 多渠道通知**: 支持 Telegram、Discord 推送

## 🚀 快速开始

### 1. Fork 本仓库

点击右上角的 "Fork" 按钮。

### 2. 配置 Secrets

在仓库的 `Settings` → `Secrets and variables` → `Actions` 中添加：

| Secret | 必需 | 说明 |
|--------|------|------|
| `DEEPSEEK_API_KEY` | ✅ | DeepSeek API 密钥 |
| `TELEGRAM_BOT_TOKEN` | ❌ | Telegram Bot Token |
| `TELEGRAM_CHAT_ID` | ❌ | Telegram Chat ID |
| `DISCORD_WEBHOOK_URL` | ❌ | Discord Webhook URL |

### 3. 启用 GitHub Pages

1. 进入 `Settings` → `Pages`
2. Source 选择 `GitHub Actions`

### 4. 运行工作流

1. 进入 `Actions` 标签页
2. 选择 "Daily Trading Intelligence (DeepSeek v2)"
3. 点击 "Run workflow"

## 📁 项目结构

```
trades-deepseek-v2/
├── .github/workflows/
│   ├── daily-trades.yml      # 每日交易简报工作流
│   └── deploy-pages.yml      # GitHub Pages 部署工作流
├── trades/
│   ├── config/
│   │   └── watchlist.json    # 监控列表配置
│   ├── scripts/
│   │   ├── collect_market_data.py     # 市场数据收集
│   │   ├── collect_congress_trades.py # 国会交易收集
│   │   ├── collect_insider_trades.py  # 内幕交易收集
│   │   ├── collect_sec_filings.py     # SEC文件收集
│   │   ├── collect_polymarket.py      # Polymarket数据收集
│   │   ├── generate_brief.py          # 简报生成
│   │   ├── generate_pages.py          # 网页生成
│   │   └── send_notifications.py      # 通知发送
│   ├── data/                 # 收集的数据 (自动生成)
│   └── output/briefs/        # 生成的简报 (自动生成)
├── docs/                     # GitHub Pages 文件 (自动生成)
└── README.md
```

## 🔧 自定义配置

### 修改监控列表

编辑 `trades/config/watchlist.json`:

```json
{
  "tickers": ["AAPL", "MSFT", "GOOGL", "NVDA"],
  "sectors": ["Technology", "AI/ML"],
  "politicians_to_watch": ["Nancy Pelosi"],
  "alert_thresholds": {
    "congress_trade_min_amount": 100000,
    "insider_trade_min_shares": 10000
  }
}
```

### 修改运行时间

编辑 `.github/workflows/daily-trades.yml` 中的 cron 表达式:

```yaml
schedule:
  - cron: '0 14 * * 1-5'  # UTC 14:00 = 北京时间 22:00
```

## 💰 成本估算

| 项目 | 月度成本 |
|-----|---------|
| GitHub Actions | 免费 (2000分钟/月) |
| DeepSeek API | ~$0.05-0.10 |
| GitHub Pages | 免费 |
| **总计** | **~$0.10/月** |

## 📊 数据源说明

| 数据源 | 方式 | 说明 |
|-------|------|------|
| Yahoo Finance | API | 免费，无需密钥 |
| Capitol Trades | 爬虫 | 国会交易数据 |
| SEC EDGAR | API | 官方披露数据 |
| Polymarket | API | 预测市场数据 |

## ⚠️ 免责声明

- 本系统仅供信息参考，**不构成投资建议**
- 所有交易决策应基于您自己的研究和风险承受能力
- 过往表现不代表未来收益
- 请遵守当地法律法规

## 🔗 相关资源

- [《个人全景监狱》原文](https://docs.google.com/document/d/19-ajYTp2hwOW9WcirY9OIoSvMdfyivup8LMI92PkS20/)
- [DeepSeek API 文档](https://api-docs.deepseek.com/)
- [Polymarket API 文档](https://docs.polymarket.com/)

## 📝 License

MIT License

---

> "Occupy the tower early. Don't let it occupy you."
