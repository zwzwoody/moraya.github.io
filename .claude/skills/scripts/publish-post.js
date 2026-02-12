/**
 * Hexo 博客文章发布脚本
 *
 * 功能：
 * 1. 创建与文章同名的资源文件夹
 * 2. 将文章中的图片移动到该文件夹
 * 3. 更新图片路径为 Hexo 格式
 * 4. 添加 front matter（标题、日期、标签）
 */

const fs = require('fs');
const path = require('path');

// 获取当前时间（Hexo 格式：2026-02-12 16:30:00）
function getCurrentDate() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

// 解析命令行参数
const postPath = process.argv[2];
const title = process.argv[3];
const tags = process.argv[4];

if (!postPath || !title) {
  console.error('用法: node publish-post.js <文章路径> <标题> [标签]');
  process.exit(1);
}

// 解析路径
let fullPath;
if (path.isAbsolute(postPath)) {
  fullPath = postPath;
} else {
  // 假设路径是相对于 source/_posts 的
  fullPath = path.join(process.cwd(), 'source', '_posts', postPath);
}

if (!fs.existsSync(fullPath)) {
  console.error(`错误: 文件不存在 ${fullPath}`);
  process.exit(1);
}

// 获取文件名和目录
const postDir = path.dirname(fullPath);
const postName = path.basename(fullPath, '.md');
const assetDirName = postName; // Hexo 格式：与文章同名（不带 .md）
const assetDirPath = path.join(postDir, assetDirName);

console.log(`处理文章: ${fullPath}`);
console.log(`资源目录: ${assetDirPath}`);

// 创建资源目录
if (!fs.existsSync(assetDirPath)) {
  fs.mkdirSync(assetDirPath, { recursive: true });
  console.log(`创建资源目录: ${assetDirPath}`);
}

// 读取文章内容
let content = fs.readFileSync(fullPath, 'utf-8');

// 定义图片匹配的正则表达式模式
// 匹配 Markdown 图片: ![alt](path)
const markdownImgRegex = /!\[([^\]]*)\]\(([^)]+)\)/g;
// 匹配 HTML 图片: <img src="path" ...>
const htmlImgRegex = /<img[^>]+src=["']([^"']+)["'][^>]*>/gi;
// 匹配已有的 asset_img 标签（避免重复处理）
const assetImgRegex = /{%\s*asset_img\s+([^%}]+)%}/g;

// 跟踪已处理的图片
const processedImages = new Set();

// 处理 Markdown 图片 - 转换为 Hexo asset_img 格式
content = content.replace(markdownImgRegex, (match, alt, imgPath) => {
  // 跳过已经处理过的或外部链接
  if (imgPath.startsWith('http') || imgPath.startsWith('/')) {
    return match;
  }

  // 跳过已经是 asset_img 格式的图片
  if (imgPath.startsWith('{%')) {
    return match;
  }

  // 获取图片文件名
  const fileName = path.basename(imgPath);

  // 获取原始图片的绝对路径
  const originalPath = path.resolve(postDir, imgPath);

  if (!fs.existsSync(originalPath)) {
    console.warn(`警告: 图片不存在 ${originalPath}`);
    // 返回转换后的格式，即使图片不存在
    return `{% asset_img ${fileName} %}`;
  }

  // 避免重复处理
  if (processedImages.has(originalPath)) {
    return `{% asset_img ${fileName} %}`;
  }
  processedImages.add(originalPath);

  // 复制图片到资源目录
  const destPath = path.join(assetDirPath, fileName);

  fs.copyFileSync(originalPath, destPath);
  console.log(`复制图片: ${fileName} -> ${assetDirName}/`);

  // 返回 Hexo asset_img 格式
  return `{% asset_img ${fileName} %}`;
});

// 处理 HTML 格式的图片 - 同样转换为 asset_img 格式
content = content.replace(htmlImgRegex, (match, imgPath) => {
  // 跳过已经处理过的或外部链接
  if (imgPath.startsWith('http') || imgPath.startsWith('/')) {
    return match;
  }

  // 获取图片文件名
  const fileName = path.basename(imgPath);

  // 获取原始图片的绝对路径
  const originalPath = path.resolve(postDir, imgPath);

  if (!fs.existsSync(originalPath)) {
    console.warn(`警告: 图片不存在 ${originalPath}`);
    // 返回转换后的格式，即使图片不存在
    return `{% asset_img ${fileName} %}`;
  }

  // 避免重复处理
  if (processedImages.has(originalPath)) {
    return `{% asset_img ${fileName} %}`;
  }
  processedImages.add(originalPath);

  // 复制图片到资源目录
  const destPath = path.join(assetDirPath, fileName);

  fs.copyFileSync(originalPath, destPath);
  console.log(`复制图片: ${fileName} -> ${assetDirName}/`);

  // 返回 Hexo asset_img 格式（替换整个 img 标签）
  return `{% asset_img ${fileName} %}`;
});

// 处理 front matter
const dateStr = getCurrentDate();
const tagList = tags ? tags.split(',').map(t => t.trim()).filter(t => t) : [];

let frontMatter = `---\ntitle: ${title}\ndate: ${dateStr}\n`;

if (tagList.length > 0) {
  frontMatter += `tags:\n`;
  tagList.forEach(tag => {
    frontMatter += `  - ${tag}\n`;
  });
}

frontMatter += `---\n\n`;

// 检查文章是否已有 front matter
const frontMatterRegex = /^---\s*\n[\s\S]*?\n---\s*\n/;
if (frontMatterRegex.test(content)) {
  // 替换现有的 front matter
  content = content.replace(frontMatterRegex, frontMatter);
  console.log('更新已存在的 front matter');
} else {
  // 在内容开头添加 front matter
  content = frontMatter + content;
  console.log('添加新的 front matter');
}

// 保存修改后的文章
fs.writeFileSync(fullPath, content, 'utf-8');
console.log(`\n文章已更新: ${fullPath}`);

// 删除已移动到资源目录的原始图片文件
processedImages.forEach(imgPath => {
  try {
    if (fs.existsSync(imgPath)) {
      fs.unlinkSync(imgPath);
      console.log(`删除原始图片: ${path.basename(imgPath)}`);
    }
  } catch (err) {
    console.warn(`无法删除 ${imgPath}: ${err.message}`);
  }
});

console.log('\n✅ 处理完成！');
console.log(`文章: ${fullPath}`);
console.log(`资源目录: ${assetDirPath}`);
console.log(`图片数量: ${processedImages.size}`);
