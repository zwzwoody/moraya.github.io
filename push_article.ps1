Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DeepSeek博客文章推送工具 (PowerShell)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. 检查当前目录..." -ForegroundColor Yellow
Set-Location "E:\new_blog"
Write-Host "当前目录: $(Get-Location)" -ForegroundColor Green
Write-Host ""

Write-Host "2. 检查Git状态..." -ForegroundColor Yellow
git status
Write-Host ""

Write-Host "3. 添加新文章到Git..." -ForegroundColor Yellow
git add source/_posts/deepseek帮我写文章.md
Write-Host "✅ 文件已添加到暂存区" -ForegroundColor Green
Write-Host ""

Write-Host "4. 提交更改..." -ForegroundColor Yellow
git commit -m "添加新文章：deepseek帮我写文章"
Write-Host ""

Write-Host "5. 推送到GitHub仓库..." -ForegroundColor Yellow
Write-Host "远程仓库: https://github.com/zwzwoody/moraya.github.io" -ForegroundColor Cyan
Write-Host "分支: main" -ForegroundColor Cyan
git push origin main
Write-Host ""

Write-Host "6. 检查推送结果..." -ForegroundColor Yellow
git status
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ 操作完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "你的文章已推送到:" -ForegroundColor Yellow
Write-Host "https://github.com/zwzwoody/moraya.github.io" -ForegroundColor Blue
Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")