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

## 注意事项

- 确保已安装 Hexo：`npm install -g hexo`
- 确保项目依赖已安装：`npm install`
- 按 `Ctrl + C` 停止服务器
