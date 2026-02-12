@echo off
echo ========================================
echo DeepSeek博客文章推送工具
echo ========================================
echo.

echo 1. 检查当前目录...
cd /d "E:\new_blog"
echo 当前目录: %cd%
echo.

echo 2. 检查Git状态...
git status
echo.

echo 3. 添加新文章到Git...
git add source/_posts/deepseek帮我写文章.md
echo 文件已添加到暂存区
echo.

echo 4. 提交更改...
git commit -m "添加新文章：deepseek帮我写文章"
echo.

echo 5. 推送到GitHub仓库...
echo 远程仓库: https://github.com/zwzwoody/moraya.github.io
echo 分支: main
git push origin main
echo.

echo 6. 检查推送结果...
git status
echo.

echo ========================================
echo 操作完成！
echo ========================================
echo.
echo 你的文章已推送到:
echo https://github.com/zwzwoody/moraya.github.io
echo.
echo 按任意键退出...
pause > nul