---
name: preview
description: 预览 Hexo 博客网站。运行 hexo clean、generate、server 命令启动本地服务器。
---

# Preview

帮助用户启动 Hexo 本地服务器，预览博客网站效果。

## 快速开始

```bash
/preview
```

## 说明

执行流程分为两步：先检查文章元信息，再启动本地预览。

### 第一步：检查文章元信息（Front Matter）

在启动预览前，先检查目标文章（或最近编辑文章）的 Front Matter 是否齐全。

#### 必填字段

- `title`
- `date`
- `tags`
- `categories`
- `description`

#### 检查规则

1. 如果文章没有 Front Matter（`---` 块），先创建 Front Matter。
2. 如果存在 Front Matter 但字段缺失，记录缺失项。
3. 对缺失字段逐项询问用户并补全：
   - `title`：询问文章标题
   - `date`：默认当前时间，允许用户覆盖
   - `tags`：让用户输入逗号分隔，转换为 YAML 列表
   - `categories`：让用户输入分类，转换为 YAML 列表
   - `description`：让用户输入一句摘要（建议 60-120 字）
4. 更新原文章并保存。
5. 告知用户补全结果，再继续预览流程。

### 第二步：启动本地预览

执行以下命令启动本地预览：

1. **hexo clean** - 清理缓存文件
2. **hexo generate** - 生成静态文件
3. **hexo server** - 启动本地服务器

默认访问地址：http://localhost:4000

## 选项

- `-p` 或 `--port`: 指定端口号，默认 4000
- `-i` 或 `--ip`: 指定 IP 地址，默认 localhost
- `-s` 或 `--skip-render`: 跳过渲染

## 示例

```
# 默认预览
/preview

# 指定端口
/preview 8080

# 跳过渲染
/preview -s
```

### 元信息补全交互示例

```
检测到文章: source/_posts/my-post.md
缺失字段: tags, description

请输入 tags（逗号分隔）: AI, Hexo, 写作
请输入 description: 分享我如何使用 AI workflow 提升博客写作效率

✅ Front Matter 已补全
继续执行预览...
```

## 输出要求

执行 `/preview` 后，最终输出需包含：

1. 元信息检查结果（完整/缺失项）
2. 若有缺失，显示已补全字段
3. 预览地址（默认 `http://localhost:4000`）
4. 停止方式（`Ctrl + C`）

## 注意事项

- 确保已安装 Hexo：`npm install -g hexo`
- 确保项目依赖已安装：`npm install`
- 按 `Ctrl + C` 停止服务器
- 如果用户不希望修改文章元信息，需先确认是否跳过检查再继续预览
