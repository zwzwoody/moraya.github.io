const fs = require('fs');
const path = require('path');

// 使用当前工作目录作为项目根目录
const projectRoot = process.cwd();

// 配置
const POSTS_DIR = path.join(projectRoot, 'source/_posts');
const BACKUP_DIR = path.join(projectRoot, 'page-tmp');

// 解析命令行参数
const args = process.argv.slice(2);
if (args.length === 0) {
    console.log('用法: node backup-post.js <文章路径>');
    console.log('示例: node backup-post.js my-post.md');
    console.log('示例: node backup-post.js 2026/new-post.md');
    process.exit(1);
}

const rawInput = args[0];
let mdFilePath = '';
let postFileName = '';
let postDir = '';

// 规范化输入路径：去除可能包含的 source/_posts 前缀
function normalizeInput(input) {
    // 统一使用正斜杠处理
    const normalized = input.replace(/\\/g, '/');
    // 如果路径已经以 source/_posts 开头，直接返回项目根目录下的该路径
    if (normalized.startsWith('source/_posts/')) {
        return path.join(projectRoot, normalized);
    }
    return normalized;
}

const inputPath = normalizeInput(rawInput);

// 判断是完整路径还是相对路径
if (path.isAbsolute(inputPath)) {
    mdFilePath = inputPath;
    postFileName = path.basename(inputPath, path.extname(inputPath));
    postDir = path.dirname(inputPath);
} else {
    mdFilePath = path.join(POSTS_DIR, inputPath);
    postFileName = path.basename(inputPath, path.extname(inputPath));
    postDir = path.dirname(mdFilePath);
}

// 验证文件是否存在
if (!fs.existsSync(mdFilePath)) {
    console.error(`错误: 文件不存在 - ${mdFilePath}`);
    process.exit(1);
}

// 创建备份目录
const backupFolder = path.join(BACKUP_DIR, postFileName);
if (!fs.existsSync(BACKUP_DIR)) {
    fs.mkdirSync(BACKUP_DIR, { recursive: true });
}
if (!fs.existsSync(backupFolder)) {
    fs.mkdirSync(backupFolder, { recursive: true });
}

// 复制 md 文件
const destMdPath = path.join(backupFolder, path.basename(mdFilePath));
fs.copyFileSync(mdFilePath, destMdPath);
console.log(`✓ 已复制: ${path.basename(mdFilePath)}`);

// 解析 md 文件中的图片引用
const mdContent = fs.readFileSync(mdFilePath, 'utf-8');
const imagePaths = extractImagePaths(mdContent, postDir);

// 复制找到的图片
if (imagePaths.length > 0) {
    console.log(`\n📷 找到 ${imagePaths.length} 个图片引用`);
    for (const imgPath of imagePaths) {
        if (fs.existsSync(imgPath)) {
            const imgFileName = path.basename(imgPath);
            const destImgPath = path.join(backupFolder, imgFileName);
            fs.copyFileSync(imgPath, destImgPath);
            console.log(`✓ 已复制图片: ${imgFileName}`);
        } else {
            console.log(`⚠ 图片不存在: ${imgPath}`);
        }
    }
}

// 检查并复制同名资源文件夹
const resourceFolder = path.join(postDir, postFileName);
if (fs.existsSync(resourceFolder) && fs.statSync(resourceFolder).isDirectory()) {
    const destResourceFolder = path.join(backupFolder, postFileName);
    copyFolderRecursive(resourceFolder, destResourceFolder);
    console.log(`✓ 已复制资源文件夹: ${postFileName}/`);
}

console.log(`\n✅ 备份完成！`);
console.log(`📁 备份位置: ${backupFolder}`);

// 提取 md 文件中的图片路径
function extractImagePaths(mdContent, baseDir) {
    const imagePaths = [];
    const imagePatterns = [
        // Markdown 图片: ![alt](path) - 使用更宽松的匹配
        /!\[([^\]]*)\]\(([^)]+)\)/g,
        // HTML img: <img src="path"> 或 <img src='path'>
        /<img[^>]+src=["']([^"']+)["']/gi,
        // Hexo asset_img: {% asset_img name %}
        /{%\s*asset_img\s+(\S+)\s*%}/g,
    ];

    for (const pattern of imagePatterns) {
        // 重置正则表达式状态
        pattern.lastIndex = 0;
        let match;
        while ((match = pattern.exec(mdContent)) !== null) {
            // Markdown 图片: match[1] 是 alt, match[2] 是路径
            // HTML img: match[1] 是路径
            // asset_img: match[1] 是路径
            const imgPath = (match[2] || match[1]).trim();

            // 跳过空路径
            if (!imgPath) continue;

            // 跳过外部链接和绝对URL
            if (imgPath.startsWith('http://') ||
                imgPath.startsWith('https://') ||
                imgPath.startsWith('//')) {
                continue;
            }

            // 解析图片路径
            let fullPath;
            // 处理 Windows 绝对路径 (C:\ 或 D:\)
            const isWinAbs = /^[a-zA-Z]:\\/.test(imgPath) || /^\\[\\]/.test(imgPath);
            if (isWinAbs || path.isAbsolute(imgPath)) {
                // 绝对路径 - 直接使用
                fullPath = imgPath;
            } else {
                // 相对路径，基于 md 文件所在目录
                fullPath = path.join(baseDir, imgPath);
                // 规范化路径（处理 .. 和 .）
                fullPath = path.normalize(fullPath);
            }

            if (!imagePaths.includes(fullPath)) {
                imagePaths.push(fullPath);
            }
        }
    }

    return imagePaths;
}

// 复制文件夹的辅助函数
function copyFolderRecursive(src, dest) {
    if (!fs.existsSync(dest)) {
        fs.mkdirSync(dest, { recursive: true });
    }

    const entries = fs.readdirSync(src, { withFileTypes: true });

    for (const entry of entries) {
        const srcPath = path.join(src, entry.name);
        const destPath = path.join(dest, entry.name);

        if (entry.isDirectory()) {
            copyFolderRecursive(srcPath, destPath);
        } else {
            fs.copyFileSync(srcPath, destPath);
        }
    }
}
