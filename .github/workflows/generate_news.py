import os
import re
from html import escape
from html.parser import HTMLParser

# 从环境变量读取时间信息
update_time = os.environ.get('UPDATE_TIME', '2026-04-10 09:28:28')
today = os.environ.get('TODAY', '2026-04-10')

# 检查 HTML 文件是否存在
if not os.path.exists('news-temp.html'):
    print('Error: news-temp.html not found')
    exit(1)

# 读取 HTML 内容
with open('news-temp.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

if not html_content.strip():
    print('Error: HTML content is empty')
    exit(1)

# 提取错误信息（如果有）
error_match = re.search(r'<div class="ai-error">(.*?)</div>', html_content, re.DOTALL)
error_html = ''
if error_match:
    error_msg = error_match.group(1)
    error_html = f'''<div class="ai-error-banner">
  <span class="error-icon">⚠️</span>
  <span class="error-text">{error_msg}</span>
</div>'''

# 提取AI分析内容
def extract_ai_analysis(html):
    """提取AI分析区块内容"""
    ai_section_match = re.search(r'<div class="ai-section">(.*?)</div>\s*</div>\s*</div>\s*(?=<div class="word-group"|$)', html, re.DOTALL)
    if not ai_section_match:
        # 尝试另一种匹配方式
        ai_section_match = re.search(r'<div class="ai-section">(.*?)</div>\s*</div>\s*</div>', html, re.DOTALL)

    if not ai_section_match:
        return ''

    ai_section_html = ai_section_match.group(1)

    # 提取AI区块标题
    ai_title_match = re.search(r'<div class="ai-section-title">([^<]+)</div>', ai_section_html)
    ai_title = ai_title_match.group(1).strip() if ai_title_match else 'AI 深度分析'

    # 提取AI徽章
    ai_badge_match = re.search(r'<div class="ai-section-badge">([^<]+)</div>', ai_section_html)
    ai_badge = ai_badge_match.group(1).strip() if ai_badge_match else 'AI'

    # 提取所有ai-block
    ai_blocks = []
    block_pattern = r'<div class="ai-block">\s*<div class="ai-block-title">([^<]+)</div>\s*<div class="ai-block-content">(.*?)</div>\s*</div>'
    for block_match in re.finditer(block_pattern, ai_section_html, re.DOTALL):
        block_title = block_match.group(1).strip()
        block_content = block_match.group(2).strip()
        # 清理HTML标签
        block_content = re.sub(r'<[^>]+>', '', block_content)
        block_content = block_content.replace('\n', ' ').replace('\r', '').replace('\t', ' ')
        block_content = re.sub(r'\s+', ' ', block_content)
        ai_blocks.append({
            'title': escape(block_title),
            'content': escape(block_content)
        })

    if not ai_blocks:
        return ''

    # 构建AI分析HTML
    blocks_html = ''
    for block in ai_blocks:
        blocks_html += f'''
<div class="ai-analysis-block">
<div class="ai-analysis-block-title">{block['title']}</div>
<div class="ai-analysis-block-content">{block['content']}</div>
</div>'''

    ai_html = f'''
<div class="ai-analysis-section">
<div class="ai-analysis-header">
<span class="ai-analysis-icon">🤖</span>
<span class="ai-analysis-title-main">{escape(ai_title)}</span>
<span class="ai-analysis-badge">{escape(ai_badge)}</span>
</div>
<div class="ai-analysis-content">
{blocks_html}
</div>
</div>'''

    return ai_html

ai_analysis_html = extract_ai_analysis(html_content)
print(f"AI analysis extracted: {'Yes' if ai_analysis_html else 'No'}")

# 提取统计信息
stats = {}
stat_patterns = [
    (r'<span class="info-label">报告类型</span>\s*<span class="info-value">([^<]+)</span>', 'report_type'),
    (r'<span class="info-label">新闻总数</span>\s*<span class="info-value">([^<]+)</span>', 'total_news'),
    (r'<span class="info-label">热点新闻</span>\s*<span class="info-value">([^<]+)</span>', 'hot_news'),
    (r'<span class="info-label">生成时间</span>\s*<span class="info-value">([^<]+)</span>', 'gen_time'),
]

for pattern, key in stat_patterns:
    match = re.search(pattern, html_content)
    if match:
        stats[key] = match.group(1).strip()

# 使用简单的字符串查找和栈来提取 word-group
def extract_word_groups(html):
    """提取所有 word-group 的内容"""
    groups = []
    idx = 0

    while True:
        # 查找 word-group 开始标签
        start_match = re.search(r'<div class="word-group">', html[idx:])
        if not start_match:
            break

        start_pos = idx + start_match.end()

        # 使用栈来找到匹配的结束标签
        depth = 1
        pos = start_pos

        while depth > 0 and pos < len(html):
            # 查找下一个开标签或闭标签
            next_open = html.find('<div', pos)
            next_close = html.find('</div>', pos)

            if next_close == -1:
                break

            if next_open != -1 and next_open < next_close:
                # 找到开标签
                # 检查是否是自闭合或注释
                tag_end = html.find('>', next_open)
                if tag_end != -1:
                    depth += 1
                pos = tag_end + 1 if tag_end != -1 else next_open + 1
            else:
                # 找到闭标签
                depth -= 1
                pos = next_close + 6  # len('</div>') = 6

        if depth == 0:
            group_content = html[start_pos:pos-6]  # 排除最后的 </div>
            groups.append(group_content)

        idx = pos

    return groups

# 提取所有 word-group
word_groups_raw = extract_word_groups(html_content)
print(f"Found {len(word_groups_raw)} word groups")

# 解析每个 word-group
word_groups = []

for group_html in word_groups_raw[:8]:  # 限制最多8个源
    # 提取源名称
    source_match = re.search(r'<div class="word-name">([^<]+)</div>', group_html)
    if not source_match:
        continue

    source_name = source_match.group(1).strip()

    # 提取数量
    count_match = re.search(r'<div class="word-count[^"]*">([^<]+)</div>', group_html)
    news_count = count_match.group(1).strip() if count_match else '0 条'

    # 提取新闻项 - 使用栈方法
    news_items = []
    idx = 0

    while True:
        # 查找 news-item 开始标签
        item_start_match = re.search(r'<div class="news-item[^"]*">', group_html[idx:])
        if not item_start_match:
            break

        start_pos = idx + item_start_match.end()

        # 使用栈来找到匹配的结束标签
        depth = 1
        pos = start_pos

        while depth > 0 and pos < len(group_html):
            next_open = group_html.find('<div', pos)
            next_close = group_html.find('</div>', pos)

            if next_close == -1:
                break

            if next_open != -1 and next_open < next_close:
                tag_end = group_html.find('>', next_open)
                if tag_end != -1:
                    depth += 1
                pos = tag_end + 1 if tag_end != -1 else next_open + 1
            else:
                depth -= 1
                pos = next_close + 6

        if depth == 0:
            news_html = group_html[start_pos:pos-6]

            # 提取排名
            rank_match = re.search(r'<span class="rank-num[^"]*">(\d+)</span>', news_html)
            rank = rank_match.group(1) if rank_match else ''

            # 提取时间
            time_match = re.search(r'<span class="time-info">([^<]+)</span>', news_html)
            time_info = time_match.group(1) if time_match else ''

            # 提取标题和链接
            title_match = re.search(r'<div class="news-title">.*?<a href="([^"]+)"[^>]*>(.*?)</a>.*?</div>', news_html, re.DOTALL)
            if title_match:
                link = title_match.group(1).strip()
                # 清理标题中的 HTML 标签
                title = re.sub(r'<[^>]+>', '', title_match.group(2)).strip()
                title = title.replace('\n', ' ').replace('\r', '').replace('\t', ' ')
                title = re.sub(r'\s+', ' ', title)  # 合并多个空格

                news_items.append({
                    'rank': rank,
                    'time': time_info,
                    'title': escape(title),
                    'link': escape(link),
                    'is_new': 'new' in item_start_match.group(0)
                })

        idx = pos

    if news_items:
        word_groups.append({
            'name': escape(source_name),
            'count': escape(news_count),
            'items': news_items[:15]  # 每个源最多15条
        })
        print(f"  - {source_name}: {len(news_items)} items")

# 构建新闻内容 HTML
news_content_html = ''
for group in word_groups:
    items_html = ''
    for item in group['items']:
        new_badge = '<span class="new-badge">NEW</span>' if item['is_new'] else ''
        rank_class = ''
        if item['rank']:
            rank_num = int(item['rank']) if item['rank'].isdigit() else 0
            if rank_num <= 3:
                rank_class = 'top'
            elif rank_num <= 5:
                rank_class = 'high'

        rank_html = f'<span class="rank-badge {rank_class}">{item["rank"]}</span>' if item['rank'] else ''

        items_html += f'''
<div class="news-item">
<div class="news-rank">{rank_html}</div>
<div class="news-body">
<a href="{item['link']}" target="_blank" class="news-title-link">{item['title']}</a>
{new_badge}
<span class="news-time">{item['time']}</span>
</div>
</div>'''

    news_content_html += f'''
<div class="source-section">
<div class="source-header">
<span class="source-name">{group['name']}</span>
<span class="source-count">{group['count']}</span>
</div>
<div class="news-list">
{items_html}
</div>
</div>'''

# 构建统计信息 HTML
stats_html = ''
if stats:
    stats_items = []
    if 'report_type' in stats:
        stats_items.append(f'<div class="stat-item"><span class="stat-label">报告类型</span><span class="stat-value">{stats["report_type"]}</span></div>')
    if 'total_news' in stats:
        stats_items.append(f'<div class="stat-item"><span class="stat-label">新闻总数</span><span class="stat-value">{stats["total_news"]}</span></div>')
    if 'hot_news' in stats:
        stats_items.append(f'<div class="stat-item"><span class="stat-label">热点新闻</span><span class="stat-value">{stats["hot_news"]}</span></div>')
    if 'gen_time' in stats:
        stats_items.append(f'<div class="stat-item"><span class="stat-label">生成时间</span><span class="stat-value">{stats["gen_time"]}</span></div>')
    stats_html = '<div class="stats-bar">' + ''.join(stats_items) + '</div>'

# 确保目标目录存在
os.makedirs('source/daily-news', exist_ok=True)

# 生成 Markdown 内容
content = f"""---
title: 每日热点
date: {update_time}
updated: {update_time}
type: "daily-news"
comments: false
---

<div class="daily-news-wrapper">
  <div class="news-header-bar">
    <span class="news-date">{today}</span>
  </div>

  {stats_html}

  {error_html}

  {ai_analysis_html}

  <div class="news-content">
{news_content_html}
  </div>

  <div class="news-footer">
    <p>数据来源：<a href="https://github.com/zwzwoody/trendradar" target="_blank">TrendRadar</a></p>
    <p class="hint">此页面每日自动同步技术热榜新闻</p>
  </div>
</div>

<style>
.daily-news-wrapper {{
  max-width: 100%;
  margin: 0 auto;
}}

.news-header-bar {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px 20px;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  border-radius: 12px;
  color: white;
}}

.news-date {{
  font-size: 16px;
  font-weight: 600;
}}

.stats-bar {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
  padding: 16px;
  background: var(--card-bg, #f8fafc);
  border-radius: 10px;
  border: 1px solid var(--border-color, #e2e8f0);
}}

.stat-item {{
  text-align: center;
}}

.stat-label {{
  display: block;
  font-size: 12px;
  color: var(--text-secondary, #64748b);
  margin-bottom: 4px;
}}

.stat-value {{
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary, #1e293b);
}}

.ai-error-banner {{
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 13px;
  color: #991b1b;
}}

.error-icon {{
  font-size: 16px;
}}

.source-section {{
  margin-bottom: 28px;
  background: var(--card-bg, white);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  border: 1px solid var(--border-color, #e5e7eb);
}}

.source-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 18px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-bottom: 1px solid var(--border-color, #e2e8f0);
}}

.source-name {{
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary, #1e293b);
}}

.source-count {{
  font-size: 13px;
  color: #dc2626;
  font-weight: 600;
  background: rgba(220, 38, 38, 0.1);
  padding: 4px 10px;
  border-radius: 12px;
}}

.news-list {{
  padding: 12px 16px;
}}

.news-item {{
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid var(--border-color, #f1f5f9);
}}

.news-item:last-child {{
  border-bottom: none;
}}

.news-rank {{
  flex-shrink: 0;
}}

.rank-badge {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  padding: 0 6px;
  background: #6b7280;
  color: white;
  font-size: 12px;
  font-weight: 700;
  border-radius: 12px;
}}

.rank-badge.top {{
  background: #dc2626;
}}

.rank-badge.high {{
  background: #ea580c;
}}

.news-body {{
  flex: 1;
  min-width: 0;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}}

.news-title-link {{
  color: var(--link-color, #2563eb);
  text-decoration: none;
  font-size: 15px;
  line-height: 1.5;
  flex: 1;
  min-width: 0;
}}

.news-title-link:hover {{
  text-decoration: underline;
  color: var(--link-hover-color, #1d4ed8);
}}

.news-title-link:visited {{
  color: var(--link-visited-color, #7c3aed);
}}

.new-badge {{
  font-size: 10px;
  font-weight: 700;
  color: #92400e;
  background: #fbbf24;
  padding: 2px 6px;
  border-radius: 4px;
  letter-spacing: 0.5px;
}}

.news-time {{
  font-size: 12px;
  color: var(--text-secondary, #94a3b8);
  white-space: nowrap;
}}

.news-footer {{
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--border-color, #e5e7eb);
  text-align: center;
  font-size: 13px;
  color: var(--text-secondary, #6b7280);
}}

.news-footer a {{
  color: #4f46e5;
  text-decoration: none;
  font-weight: 500;
}}

.news-footer a:hover {{
  text-decoration: underline;
}}

.news-footer .hint {{
  margin-top: 8px;
  color: var(--text-tertiary, #9ca3af);
  font-size: 12px;
}}

/* 深色模式适配 */
[data-theme="dark"] .stats-bar {{
  background: rgba(255,255,255,0.05);
  border-color: rgba(255,255,255,0.1);
}}

[data-theme="dark"] .stat-label {{
  color: #94a3b8;
}}

[data-theme="dark"] .stat-value {{
  color: #f1f5f9;
}}

[data-theme="dark"] .source-section {{
  background: rgba(255,255,255,0.03);
  border-color: rgba(255,255,255,0.1);
}}

[data-theme="dark"] .source-header {{
  background: linear-gradient(135deg, rgba(248,250,252,0.08) 0%, rgba(241,245,249,0.05) 100%);
  border-color: rgba(255,255,255,0.1);
}}

[data-theme="dark"] .source-name {{
  color: #f1f5f9;
}}

[data-theme="dark"] .news-item {{
  border-color: rgba(255,255,255,0.08);
}}

[data-theme="dark"] .news-title-link {{
  color: #60a5fa;
}}

[data-theme="dark"] .news-title-link:hover {{
  color: #93c5fd;
}}

[data-theme="dark"] .news-title-link:visited {{
  color: #c4b5fd;
}}

[data-theme="dark"] .news-time {{
  color: #64748b;
}}

[data-theme="dark"] .news-footer {{
  border-color: rgba(255,255,255,0.1);
  color: #9ca3af;
}}

/* AI分析区块样式 */
.ai-analysis-section {{
  margin-bottom: 28px;
  background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(79, 70, 229, 0.15);
  border: 1px solid rgba(99, 102, 241, 0.2);
}}

.ai-analysis-header {{
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 18px 24px;
  background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
  border-bottom: 1px solid rgba(255,255,255,0.1);
}}

.ai-analysis-icon {{
  font-size: 24px;
}}

.ai-analysis-title-main {{
  font-size: 18px;
  font-weight: 600;
  color: #fff;
  flex: 1;
}}

.ai-analysis-badge {{
  font-size: 11px;
  font-weight: 700;
  color: #a5b4fc;
  background: rgba(99, 102, 241, 0.3);
  padding: 4px 10px;
  border-radius: 12px;
  border: 1px solid rgba(99, 102, 241, 0.5);
}}

.ai-analysis-content {{
  padding: 20px 24px;
}}

.ai-analysis-block {{
  margin-bottom: 16px;
  padding: 16px;
  background: rgba(255,255,255,0.05);
  border-radius: 12px;
  border-left: 3px solid #6366f1;
}}

.ai-analysis-block:last-child {{
  margin-bottom: 0;
}}

.ai-analysis-block-title {{
  font-size: 14px;
  font-weight: 600;
  color: #a5b4fc;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}}

.ai-analysis-block-content {{
  font-size: 15px;
  color: rgba(255,255,255,0.9);
  line-height: 1.7;
}}

/* AI分析深色模式适配 */
[data-theme="dark"] .ai-analysis-section {{
  background: linear-gradient(135deg, #0f0d2e 0%, #1e1b4b 100%);
  border-color: rgba(99, 102, 241, 0.3);
}}

/* 移动端适配 */
@media (max-width: 640px) {{
  .news-header-bar {{
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }}

  .stats-bar {{
    grid-template-columns: repeat(2, 1fr);
  }}

  .news-body {{
    flex-direction: column;
    align-items: flex-start;
  }}

  .news-time {{
    margin-left: auto;
  }}

  .ai-analysis-header {{
    padding: 14px 18px;
  }}

  .ai-analysis-title-main {{
    font-size: 16px;
  }}

  .ai-analysis-content {{
    padding: 16px 18px;
  }}

  .ai-analysis-block {{
    padding: 12px;
  }}
}}
</style>
"""

# 写入文件
with open('source/daily-news/index.md', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'News page generated successfully at {update_time}')
print(f'Parsed {len(word_groups)} news sources with {sum(len(g["items"]) for g in word_groups)} total items')
