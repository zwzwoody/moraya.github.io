---
title: 每日热点
date: 2026-04-07 15:15:29
updated: 2026-04-07 15:15:29
type: "daily-news"
comments: false
---

<div class="daily-news-wrapper">
  <div class="news-header-bar">
    <div class="news-title-section">
      <h1 class="page-title">📰 每日热点</h1>
      <span class="news-date">2026-04-07</span>
    </div>
    <span class="update-badge">🔄 更新于 2026-04-07 15:15:29</span>
  </div>

  <div class="stats-bar"><div class="stat-item"><span class="stat-label">报告类型</span><span class="stat-value">全天汇总</span></div><div class="stat-item"><span class="stat-label">新闻总数</span><span class="stat-value">175 条</span></div><div class="stat-item"><span class="stat-label">热点新闻</span><span class="stat-value">59 条</span></div><div class="stat-item"><span class="stat-label">生成时间</span><span class="stat-value">04-07 20:26</span></div></div>

  <div class="ai-error-banner">
  <span class="error-icon">⚠️</span>
  <span class="error-text">⚠️ AI 分析失败: AI 分析失败 (BadRequestError): litellm.BadRequestError: DeepseekException - {&quot;error&quot;:{&quot;message&quot;:&quot;Model Not Exist&quot;,&quot;type&quot;:&quot;invalid_request_error&quot;,&quot;param&quot;:null,&quot;code&quot;:&quot;invalid_request_error&quot;}}</span>
</div>

  <div class="news-content">
    
  </div>

  <div class="news-footer">
    <p>数据来源：<a href="https://github.com/zwzwoody/trendradar" target="_blank">TrendRadar</a></p>
    <p class="hint">此页面每日自动同步技术热榜新闻</p>
  </div>
</div>

<style>
.daily-news-wrapper {
  max-width: 100%;
  margin: 0 auto;
}

.news-header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px 20px;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  border-radius: 12px;
  color: white;
}

.news-title-section {
  display: flex;
  align-items: center;
  gap: 16px;
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
}

.news-date {
  font-size: 16px;
  opacity: 0.9;
}

.update-badge {
  font-size: 13px;
  opacity: 0.85;
  background: rgba(255,255,255,0.15);
  padding: 6px 12px;
  border-radius: 20px;
}

.stats-bar {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
  padding: 16px;
  background: var(--card-bg, #f8fafc);
  border-radius: 10px;
  border: 1px solid var(--border-color, #e2e8f0);
}

.stat-item {
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: var(--text-secondary, #64748b);
  margin-bottom: 4px;
}

.stat-value {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary, #1e293b);
}

.ai-error-banner {
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
}

.error-icon {
  font-size: 16px;
}

.source-section {
  margin-bottom: 28px;
  background: var(--card-bg, white);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  border: 1px solid var(--border-color, #e5e7eb);
}

.source-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 18px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-bottom: 1px solid var(--border-color, #e2e8f0);
}

.source-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary, #1e293b);
}

.source-count {
  font-size: 13px;
  color: #dc2626;
  font-weight: 600;
  background: rgba(220, 38, 38, 0.1);
  padding: 4px 10px;
  border-radius: 12px;
}

.news-list {
  padding: 12px 16px;
}

.news-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid var(--border-color, #f1f5f9);
}

.news-item:last-child {
  border-bottom: none;
}

.news-rank {
  flex-shrink: 0;
}

.rank-badge {
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
}

.rank-badge.top {
  background: #dc2626;
}

.rank-badge.high {
  background: #ea580c;
}

.news-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}

.news-title-link {
  color: var(--link-color, #2563eb);
  text-decoration: none;
  font-size: 15px;
  line-height: 1.5;
  flex: 1;
  min-width: 0;
}

.news-title-link:hover {
  text-decoration: underline;
  color: var(--link-hover-color, #1d4ed8);
}

.news-title-link:visited {
  color: var(--link-visited-color, #7c3aed);
}

.new-badge {
  font-size: 10px;
  font-weight: 700;
  color: #92400e;
  background: #fbbf24;
  padding: 2px 6px;
  border-radius: 4px;
  letter-spacing: 0.5px;
}

.news-time {
  font-size: 12px;
  color: var(--text-secondary, #94a3b8);
  white-space: nowrap;
}

.news-footer {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--border-color, #e5e7eb);
  text-align: center;
  font-size: 13px;
  color: var(--text-secondary, #6b7280);
}

.news-footer a {
  color: #4f46e5;
  text-decoration: none;
  font-weight: 500;
}

.news-footer a:hover {
  text-decoration: underline;
}

.news-footer .hint {
  margin-top: 8px;
  color: var(--text-tertiary, #9ca3af);
  font-size: 12px;
}

/* 深色模式适配 */
[data-theme="dark"] .stats-bar {
  background: rgba(255,255,255,0.05);
  border-color: rgba(255,255,255,0.1);
}

[data-theme="dark"] .stat-label {
  color: #94a3b8;
}

[data-theme="dark"] .stat-value {
  color: #f1f5f9;
}

[data-theme="dark"] .source-section {
  background: rgba(255,255,255,0.03);
  border-color: rgba(255,255,255,0.1);
}

[data-theme="dark"] .source-header {
  background: linear-gradient(135deg, rgba(248,250,252,0.08) 0%, rgba(241,245,249,0.05) 100%);
  border-color: rgba(255,255,255,0.1);
}

[data-theme="dark"] .source-name {
  color: #f1f5f9;
}

[data-theme="dark"] .news-item {
  border-color: rgba(255,255,255,0.08);
}

[data-theme="dark"] .news-title-link {
  color: #60a5fa;
}

[data-theme="dark"] .news-title-link:hover {
  color: #93c5fd;
}

[data-theme="dark"] .news-title-link:visited {
  color: #c4b5fd;
}

[data-theme="dark"] .news-time {
  color: #64748b;
}

[data-theme="dark"] .news-footer {
  border-color: rgba(255,255,255,0.1);
  color: #9ca3af;
}

/* 移动端适配 */
@media (max-width: 640px) {
  .news-header-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .news-title-section {
    flex-direction: column;
    gap: 8px;
  }

  .page-title {
    font-size: 20px;
  }

  .stats-bar {
    grid-template-columns: repeat(2, 1fr);
  }

  .news-body {
    flex-direction: column;
    align-items: flex-start;
  }

  .news-time {
    margin-left: auto;
  }
}
</style>
