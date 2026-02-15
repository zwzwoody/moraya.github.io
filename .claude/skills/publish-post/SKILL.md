---
name: publish-post
description: 发布 Hexo 博客文章。用于整理图片资源、添加 front matter、推送到 GitHub。
---

# Publish Post

帮助用户发布 Hexo 博客文章，自动完成图片整理、格式转换和 Git 推送。

## 快速开始

```bash
/publish-post
文章路径: my-post.md
标题: 我的新文章
标签: 技术,前端
推送到 GitHub？(y/n): y
```

## 说明

### 第一步：输入文章路径

提示用户输入 markdown 文件的路径，支持：
- 相对于 `source/_posts` 的路径：`my-post.md`、`folder/post.md`
- 完整路径：`E:\blog\source\_posts\my-post.md`

### 第二步：输入文章标题

提示用户输入文章标题，用于：
- front matter 中的 `title` 字段
- git commit 消息

### 第三步：输入文章标签

提示用户输入标签（逗号分隔），自动格式化为 YAML 数组：
- 输入：`技术,前端,Hexo`
- 输出：
  ```yaml
  tags:
    - 技术
    - 前端
    - Hexo
  ```

### 第四步：备份原文件

调用 backup-post skill 备份原文件到 `pages-tmp/<文件名>/`：
- 备份 .md 文件
- 解析并备份 md 文件中引用的图片（支持 Markdown、HTML、asset_img 格式）
- 备份同名资源文件夹（如果存在）

### 第五步：执行处理脚本

运行 `node .claude/skills/scripts/publish-post.js`，自动：

2. **创建资源文件夹**：
   - 在 `source/_posts/` 下创建与文章同名的文件夹
   - 用于存放 Hexo 资源图片

3. **处理图片**：
   - 匹配 Markdown 图片：`![alt](path)` → `{% asset_img fileName %}`
   - 匹配 HTML 图片：`<img src="path">` → `{% asset_img fileName %}`
   - 跳过：外部链接、已处理图片、asset_img 格式
   - 复制图片到资源文件夹
   - 删除原始图片文件

4. **添加/更新 front matter**：
   - 添加 `title`、`date`、`tags` 字段
   - 如果已存在则更新

### 第六步：确认推送 GitHub

询问用户是否推送到 GitHub：
- 输入 `y` 或 `Y`：执行推送
- 输入 `n` 或其他：跳过推送

### 第七步：执行 Git 操作

当用户确认后执行：
```bash
git add .
git commit -m "Add post: <文章标题>"
git push
```

## 流程图

```
用户输入
    ↓
文章路径 → 验证文件是否存在
    ↓
文章标题
    ↓
标签（可选）
    ↓
调用 backup-post 备份原文件
    ↓
执行 publish-post.js 脚本
    ├── 创建资源文件夹
    ├── 处理图片（Markdown + HTML）
    ├── 更新为 asset_img 格式
    ├── 添加 front matter
    └── 保存文件
    ↓
是否推送到 GitHub？(y/n)
    ├── y → git add → commit → push
    └── n → 完成
```

## 示例

### 基本使用

```
输入文章路径: hello-world.md
输入文章标题: 你好世界
输入文章标签: 随笔
是否推送到 GitHub？(y/n): y
```

### 带文件夹路径

```
输入文章路径: 2026/new-post.md
输入文章标题: 2026年新文章
输入文章标签: 年度总结,技术
是否推送到 GitHub？(y/n): n
```

### 完整路径

```
输入文章路径: E:\blog\source\_posts\my-post.md
输入文章标题: 我的文章
输入文章标签:
是否推送到 GitHub？(y/n): y
```

## 备份说明

处理前会自动调用 [backup-post](../backup-post/SKILL.md) 备份到 `pages-tmp/` 目录：

```
pages-tmp/
└── my-post/                  # 与博客文件名一致
    ├── my-post.md           # 原始文章
    ├── image1.png           # 引用的图片
    └── my-post/             # 资源文件夹（如果有）
        ├── image2.png
        └── image3.jpg
```

如需恢复，从 `pages-tmp/` 复制文件回 `source/_posts/` 即可。

## 文件结构

```
.claude/skills/publish-post/
├── SKILL.md                    # 本文档
├── publish-post.json           # Skill 配置
└── scripts/
    └── publish-post.js         # 处理脚本
```

## 最佳实践

1. **输入文章路径前确认文件存在**，脚本会验证但提前检查更友好
2. **标签用逗号分隔**，会自动去除空格
3. **空标签可以直接回车**
4. **处理后检查效果**，不满意可从 `pages-tmp/` 恢复

## 故障排除

**文件不存在错误**：
- 检查路径是否正确
- 确认文件在 `source/_posts/` 目录下
- 尝试使用完整路径

**图片未处理**：
- 检查图片是否为外部链接（http://、/ 开头）
- 检查是否已是 `{% asset_img %}` 格式
- 确认图片文件实际存在

**Git 推送失败**：
- 检查网络连接
- 确认 git 远程仓库配置正确
- 检查是否有未提交的冲突

## 依赖

- Node.js（用于运行脚本）
- Git（用于版本控制）
- Hexo 项目结构（`source/_posts/` 目录）
