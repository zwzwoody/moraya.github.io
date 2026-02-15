---
name: backup-post
description: 备份博客文章到 pages-tmp 目录。用于在编辑文章前保存原始版本，文件夹名称与文件名一致。
---

# Backup Post

帮助用户备份正在编辑的博客文章到 `pages-tmp` 目录，便于版本管理和恢复。

## 快速开始

```bash
/backup-post
文章路径: my-post.md
```

## 说明

### 第一步：输入文章路径

提示用户输入需要备份的 markdown 文件路径，支持：
- 相对于 `source/_posts` 的路径：`my-post.md`、`folder/post.md`
- 完整路径：`E:\blog\source\_posts\my-post.md`

### 第二步：执行备份

运行 `node .claude/skills/scripts/backup-post.js`，自动：

1. **创建备份文件夹**：
   - 路径：`pages-tmp/<文件名>/`
   - 文件名使用原始 markdown 文件名（不含扩展名）

2. **复制文件**：
   - 复制 .md 文件到备份文件夹
   - 自动提取并复制 md 文件中引用的图片（支持多种格式）
   - 如果存在同名资源文件夹（如 `my-post/`），一并复制

3. **支持的图片格式**：
   - Markdown 图片：`![alt](image.png)`
   - HTML 图片：`<img src="image.png">`
   - Hexo asset_img：`{% asset_img image.png %}`
   - 支持绝对路径和相对路径

4. **备份结构示例**：

```
pages-tmp/
└── my-post/                  # 与博客文件名一致
    ├── my-post.md           # 博客文章
    ├── image1.png           # 引用的图片
    └── my-post/             # 资源文件夹（如果有）
        ├── image2.png
        └── image3.jpg
```

### 第三步：完成提示

告知用户备份位置，提示如需恢复可从 `pages-tmp/` 复制文件回 `source/_posts/`

## 流程图

```
用户输入
    ↓
文章路径 → 验证文件是否存在
    ↓
执行 backup-post.js 脚本
    ├── 创建 pages-tmp/<文件名>/ 目录
    ├── 复制 .md 文件
    ├── 解析并复制引用的图片
    └── 复制资源文件夹（如果有）
    ↓
完成 → 提示备份位置
```

## 示例

### 基本使用

```
输入文章路径: hello-world.md
✅ 已备份到: pages-tmp/hello-world/
```

### 带文件夹路径

```
输入文章路径: 2026/new-post.md
✅ 已备份到: pages-tmp/new-post/
```

### 完整路径

```
输入文章路径: E:\blog\source\_posts\my-post.md
✅ 已备份到: pages-tmp/my-post/
```

## 恢复说明

如需恢复备份：

1. 从 `pages-tmp/<文件名>/` 复制文件
2. 粘贴回 `source/_posts/` 覆盖原文件

```
pages-tmp/hello-world/hello-world.md  →  source/_posts/hello-world.md
pages-tmp/hello-world/hello-world/    →  source/_posts/hello-world/
```

## 文件结构

```
.claude/skills/backup-post/
├── SKILL.md                    # 本文档
└── scripts/
    └── backup-post.js         # 处理脚本
```

## 最佳实践

1. **编辑前先备份**，防止误操作导致内容丢失
2. **重要修改前备份**，可创建多个版本
3. **备份后继续编辑**，原文件位置不变

## 故障排除

**文件不存在错误**：
- 检查路径是否正确
- 确认文件在 `source/_posts/` 目录下
- 尝试使用完整路径

**备份失败**：
- 检查 `pages-tmp/` 目录是否有写入权限
- 确认磁盘空间充足
