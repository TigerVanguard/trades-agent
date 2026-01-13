#!/usr/bin/env python3
"""
GitHub Pages 生成脚本
将交易简报转换为美观的网页
"""

import json
import os
import glob
from datetime import datetime

os.makedirs('docs', exist_ok=True)
os.makedirs('docs/briefs', exist_ok=True)
os.makedirs('docs/css', exist_ok=True)

print("🌐 生成 GitHub Pages...")

# CSS 样式
css_content = """
:root {
    --bg-primary: #0d1117;
    --bg-secondary: #161b22;
    --bg-tertiary: #21262d;
    --text-primary: #c9d1d9;
    --text-secondary: #8b949e;
    --accent-green: #3fb950;
    --accent-red: #f85149;
    --accent-blue: #58a6ff;
    --accent-yellow: #d29922;
    --border-color: #30363d;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border-color);
    padding: 20px 0;
    margin-bottom: 30px;
}

header h1 {
    font-size: 1.8rem;
    color: var(--text-primary);
}

header .subtitle {
    color: var(--text-secondary);
    font-size: 0.9rem;
    margin-top: 5px;
}

.dashboard {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 20px;
}

.card h3 {
    font-size: 0.9rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 10px;
}

.card .value {
    font-size: 2rem;
    font-weight: 600;
    color: var(--text-primary);
}

.card .change {
    font-size: 0.9rem;
    margin-top: 5px;
}

.card .change.positive { color: var(--accent-green); }
.card .change.negative { color: var(--accent-red); }

.brief-content {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 30px;
}

.brief-content h1, .brief-content h2, .brief-content h3 {
    color: var(--text-primary);
    margin-top: 24px;
    margin-bottom: 16px;
}

.brief-content h1 { font-size: 1.8rem; border-bottom: 1px solid var(--border-color); padding-bottom: 10px; }
.brief-content h2 { font-size: 1.4rem; }
.brief-content h3 { font-size: 1.1rem; }

.brief-content p {
    margin-bottom: 16px;
}

.brief-content ul, .brief-content ol {
    margin-left: 20px;
    margin-bottom: 16px;
}

.brief-content li {
    margin-bottom: 8px;
}

.brief-content code {
    background: var(--bg-tertiary);
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 0.9em;
}

.brief-content pre {
    background: var(--bg-tertiary);
    padding: 16px;
    border-radius: 6px;
    overflow-x: auto;
    margin-bottom: 16px;
}

.brief-content table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 16px;
}

.brief-content th, .brief-content td {
    border: 1px solid var(--border-color);
    padding: 10px;
    text-align: left;
}

.brief-content th {
    background: var(--bg-tertiary);
}

.brief-content strong {
    color: var(--accent-blue);
}

.brief-content blockquote {
    border-left: 3px solid var(--accent-blue);
    padding-left: 16px;
    margin: 16px 0;
    color: var(--text-secondary);
}

.archive {
    margin-top: 30px;
}

.archive h2 {
    margin-bottom: 20px;
}

.archive-list {
    list-style: none;
}

.archive-list li {
    padding: 12px 16px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    margin-bottom: 10px;
}

.archive-list a {
    color: var(--accent-blue);
    text-decoration: none;
}

.archive-list a:hover {
    text-decoration: underline;
}

footer {
    margin-top: 40px;
    padding: 20px 0;
    border-top: 1px solid var(--border-color);
    text-align: center;
    color: var(--text-secondary);
    font-size: 0.85rem;
}

.tag {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 500;
}

.tag.buy { background: rgba(63, 185, 80, 0.2); color: var(--accent-green); }
.tag.sell { background: rgba(248, 81, 73, 0.2); color: var(--accent-red); }
.tag.hold { background: rgba(210, 153, 34, 0.2); color: var(--accent-yellow); }
.tag.watch { background: rgba(88, 166, 255, 0.2); color: var(--accent-blue); }

@media (max-width: 768px) {
    .container { padding: 15px; }
    .brief-content { padding: 20px; }
}
"""

# 保存CSS
with open('docs/css/style.css', 'w') as f:
    f.write(css_content)

# 读取最新简报
try:
    with open('trades/output/briefs/latest.md', 'r') as f:
        latest_brief = f.read()
except:
    latest_brief = "# 暂无简报\n\n请等待系统生成第一份简报。"

# 读取市场数据
try:
    with open('trades/data/market_snapshot.json', 'r') as f:
        market_data = json.load(f)
except:
    market_data = {"indices": {}, "market_data": {}}

# 简单的 Markdown 转 HTML
def md_to_html(md_text):
    import re
    
    # 移除 YAML front matter
    md_text = re.sub(r'^---\n.*?\n---\n', '', md_text, flags=re.DOTALL)
    
    html = md_text
    
    # 标题
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # 粗体和斜体
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # 代码块
    html = re.sub(r'```(\w*)\n(.*?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    
    # 列表
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*</li>\n)+', r'<ul>\g<0></ul>', html)
    
    # 段落
    paragraphs = html.split('\n\n')
    processed = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<'):
            p = f'<p>{p}</p>'
        processed.append(p)
    html = '\n'.join(processed)
    
    return html

# 生成首页
indices = market_data.get('indices', {})
sp500 = indices.get('S&P 500', {})
nasdaq = indices.get('NASDAQ', {})
vix = indices.get('VIX', {})

index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trading Intelligence Dashboard</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <h1>📊 Trading Intelligence Dashboard</h1>
            <p class="subtitle">基于《个人全景监狱》构建的自动化交易情报系统</p>
        </div>
    </header>
    
    <main class="container">
        <section class="dashboard">
            <div class="card">
                <h3>S&P 500</h3>
                <div class="value">{sp500.get('price', 'N/A')}</div>
                <div class="change {'positive' if str(sp500.get('change_percent', '')).startswith('-') == False else 'negative'}">
                    {sp500.get('change_percent', 'N/A')}%
                </div>
            </div>
            <div class="card">
                <h3>NASDAQ</h3>
                <div class="value">{nasdaq.get('price', 'N/A')}</div>
                <div class="change {'positive' if str(nasdaq.get('change_percent', '')).startswith('-') == False else 'negative'}">
                    {nasdaq.get('change_percent', 'N/A')}%
                </div>
            </div>
            <div class="card">
                <h3>VIX 恐慌指数</h3>
                <div class="value">{vix.get('price', 'N/A')}</div>
                <div class="change">波动率指标</div>
            </div>
            <div class="card">
                <h3>最后更新</h3>
                <div class="value" style="font-size: 1.2rem;">{datetime.now().strftime('%Y-%m-%d')}</div>
                <div class="change">{datetime.now().strftime('%H:%M UTC')}</div>
            </div>
        </section>
        
        <section class="brief-content">
            {md_to_html(latest_brief)}
        </section>
        
        <section class="archive">
            <h2>📁 历史简报</h2>
            <ul class="archive-list">
"""

# 获取所有历史简报
brief_files = sorted(glob.glob('trades/output/briefs/brief_*.md'), reverse=True)
for brief_file in brief_files[:10]:  # 最近10份
    date = os.path.basename(brief_file).replace('brief_', '').replace('.md', '')
    index_html += f'                <li><a href="briefs/{date}.html">📄 {date} 交易简报</a></li>\n'

index_html += """
            </ul>
        </section>
    </main>
    
    <footer>
        <div class="container">
            <p>🤖 由 DeepSeek AI 驱动 | 数据每日自动更新</p>
            <p>⚠️ 本系统仅供参考，不构成投资建议</p>
        </div>
    </footer>
</body>
</html>
"""

with open('docs/index.html', 'w') as f:
    f.write(index_html)

# 为每份简报生成独立页面
for brief_file in brief_files:
    date = os.path.basename(brief_file).replace('brief_', '').replace('.md', '')
    with open(brief_file, 'r') as f:
        content = f.read()
    
    brief_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>交易简报 - {date}</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <h1>📊 交易简报 - {date}</h1>
            <p class="subtitle"><a href="../index.html" style="color: var(--accent-blue);">← 返回首页</a></p>
        </div>
    </header>
    
    <main class="container">
        <section class="brief-content">
            {md_to_html(content)}
        </section>
    </main>
    
    <footer>
        <div class="container">
            <p>🤖 由 DeepSeek AI 驱动</p>
        </div>
    </footer>
</body>
</html>
"""
    
    with open(f'docs/briefs/{date}.html', 'w') as f:
        f.write(brief_html)

print(f"✓ GitHub Pages 已生成: docs/index.html")
print(f"✓ 生成了 {len(brief_files)} 份简报页面")
