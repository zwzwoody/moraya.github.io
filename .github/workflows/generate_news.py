import os
import base64

# 从环境变量读取时间信息
update_time = os.environ.get('UPDATE_TIME', '')
today = os.environ.get('TODAY', '')

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

# 对 HTML 进行 base64 编码，避免引号和特殊字符问题
html_b64 = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')

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
  <div class="news-meta">
    <span class="news-date">📅 {today}</span>
    <span class="update-time">🔄 更新时间: {update_time}</span>
  </div>

  <div class="news-iframe-container">
    <iframe id="news-frame" src="data:text/html;base64,{html_b64}" frameborder="0" scrolling="no"></iframe>
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

.news-meta {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  border-radius: 8px;
  color: white;
  font-size: 14px;
}}

.news-date {{ font-weight: 600; }}
.update-time {{ opacity: 0.9; font-size: 13px; }}

.news-iframe-container {{
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 16px rgba(0,0,0,0.06);
}}

#news-frame {{
  width: 100%;
  min-height: 800px;
  border: none;
}}

.news-footer {{
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #eee;
  text-align: center;
  font-size: 13px;
  color: #666;
}}

.news-footer .hint {{ margin-top: 8px; color: #999; font-size: 12px; }}

[data-theme="dark"] .news-iframe-container {{ background: #1a1a1a; }}
[data-theme="dark"] .news-footer {{ border-top-color: #333; color: #999; }}
</style>

<script>
window.addEventListener('load', function() {{
  var iframe = document.getElementById('news-frame');
  if (iframe) {{
    try {{
      iframe.style.height = iframe.contentWindow.document.body.scrollHeight + 'px';
    }} catch(e) {{
      iframe.style.height = '800px';
    }}
  }}
}});
</script>
"""

# 写入文件
with open('source/daily-news/index.md', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'News page generated successfully at {update_time}')
print(f'HTML size: {len(html_content)} chars, Base64 size: {len(html_b64)} chars')
