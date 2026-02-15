---
name: skill-writer
description: 帮助用户创建 Claude Code 的 Agent Skill。用于用户想要创建、写作、设计新 Skill 时，或需要 SKILL.md 文件、frontmatter、skill 结构方面的帮助。
---

# Skill Writer

这个 Skill 帮助你创建结构良好的 Agent Skill，符合最佳实践和验证要求。

## 何时使用此 Skill

在以下情况使用：
- 创建新的 Agent Skill
- 编写或更新 SKILL.md 文件
- 设计 skill 结构和 frontmatter
- 排查 skill 发现问题
- 将现有提示词或工作流转换为 Skill

## 说明

### 第一步：确定 Skill 范围

首先，理解这个 Skill 应该做什么：

1. **提出澄清问题**：
   - 这个 Skill 应该提供什么具体功能？
   - Claude 什么时候应该使用这个 Skill？
   - 它需要什么工具或资源？
   - 这是个人使用还是团队共享？

2. **保持专注**：一个 Skill = 一个功能
   - 好例子："PDF 表单填写"、"Excel 数据分析"
   - 太宽泛："文档处理"、"数据工具"

### 第二步：选择 Skill 位置

确定在哪里创建 Skill：

**个人 Skills** (`~/.claude/skills/`)：
- 个人工作流和偏好
- 实验性 Skills
- 个人生产力工具

**项目 Skills** (`.claude/skills/`)：
- 团队工作流和约定
- 项目特定专业知识
- 共享实用工具（提交到 git）

### 第三步：创建 Skill 结构

创建目录和文件：

```bash
# 个人
mkdir -p ~/.claude/skills/skill-name

# 项目
mkdir -p .claude/skills/skill-name
```

对于多文件 Skills：
```
skill-name/
├── SKILL.md (必需)
├── reference.md (可选)
├── examples.md (可选)
├── scripts/
│   └── helper.py (可选)
└── templates/
    └── template.txt (可选)
```

### 第四步：编写 SKILL.md frontmatter

使用必需字段创建 YAML frontmatter：

```yaml
---
name: skill-name
description: 简要描述这个 Skill 做什么以及何时使用
---
```

**字段要求**：

- **name**：
  - 只能用小写字母、数字、连字符
  - 最多 64 个字符
  - 必须与目录名匹配
  - 好例子：`pdf-processor`、`git-commit-helper`
  - 坏例子：`PDF_Processor`、`Git Commits!`

- **description**：
  - 最多 1024 个字符
  - 必须包含它做什么以及何时使用
  - 使用用户会说的具体触发词
  - 提及文件类型、操作和上下文

**可选 frontmatter 字段**：

- **allowed-tools**：限制工具访问（逗号分隔列表）
  ```yaml
  allowed-tools: Read, Grep, Glob
  ```
  用于：
  - 只读 Skills
  - 安全敏感工作流
  - 有限范围操作

### 第五步：编写有效的描述

描述对于 Claude 发现你的 Skill 至关重要。

**公式**：`[它做什么] + [何时使用] + [关键触发词]`

**示例**：

✅ **好例子**：
```yaml
description: 从 PDF 文件中提取文本和表格，填写表单，合并文档。当处理 PDF 文件或用户提到 PDF、表单或文档提取时使用。
```

✅ **好例子**：
```yaml
description: 分析 Excel 电子数据表，创建数据透视表和生成图表。当处理 Excel 文件、电子表格或分析 .xlsx 格式的表格数据时使用。
```

❌ **太模糊**：
```yaml
description: 帮助处理文档
description: 用于数据分析
```

**提示**：
- 包含具体的文件扩展名（.pdf、.xlsx、.json）
- 提到常见用户短语（"analyze"、"extract"、"generate"）
- 列出具体操作（不是泛泛的动词）
- 添加上下文线索（"Use when..."、"For..."）

### 第六步：构建 Skill 内容

使用清晰的 Markdown 部分：

```markdown
# Skill Name

简要概述这个 Skill 做什么。

## 快速开始

提供立即开始的简单示例。

## 说明

Claude 的逐步指导：
1. 第一步，明确操作
2. 第二步，预期结果
3. 处理边缘情况

## 示例

显示具体的使用示例，包括代码或命令。

## 最佳实践

- 要遵循的关键约定
- 要避免的常见陷阱
- 何时使用与何时不使用

## 要求

列出任何依赖项或先决条件：
```bash
pip install package-name
```

## 高级用法

对于复杂场景，请参阅 [reference.md](reference.md)。
```

### 第七步：添加支持文件（可选）

为渐进式披露创建附加文件：

**reference.md**：详细的 API 文档、高级选项
**examples.md**：扩展示例和用例
**scripts/**：辅助脚本和实用工具
**templates/**：文件模板或样板代码

从 SKILL.md 引用它们：
```markdown
高级用法，请参阅 [reference.md](reference.md)。

运行辅助脚本：
```bash
python scripts/helper.py input.txt
```
```

### 第八步：验证 Skill

检查这些要求：

✅ **文件结构**：
- [ ] SKILL.md 存在于正确位置
- [ ] 目录名与 frontmatter `name` 匹配

✅ **YAML frontmatter**：
- [ ] 第 1 行是 opening `---`
- [ ] 内容前是 closing `---`
- [ ] 有效的 YAML（无制表符、正确的缩进）
- [ ] `name` 遵循命名规则
- [ ] `description` 具体且 < 1024 个字符

✅ **内容质量**：
- [ ] 对 Claude 的说明清晰
- [ ] 提供了具体示例
- [ ] 处理了边缘情况
- [ ] 列出了依赖项（如果有）

✅ **测试**：
- [ ] 描述与用户问题匹配
- [ ] Skill 在相关查询时激活
- [ ] 说明清晰且可操作

### 第九步：测试 Skill

1. **重启 Claude Code**（如果正在运行）以加载 Skill

2. **提出匹配描述的相关问题**：
   ```
   你能帮我从这个 PDF 中提取文本吗？
   ```

3. **验证激活**：Claude 应该自动使用 Skill

4. **检查行为**：确认 Claude 正确遵循说明

### 第十步：如有需要进行调试

如果 Claude 不使用 Skill：

1. **使描述更具体**：
   - 添加触发词
   - 包含文件类型
   - 提到常见用户短语

2. **检查文件位置**：
   ```bash
   ls ~/.claude/skills/skill-name/SKILL.md
   ls .claude/skills/skill-name/SKILL.md
   ```

3. **验证 YAML**：
   ```bash
   cat SKILL.md | head -n 10
   ```

4. **运行调试模式**：
   ```bash
   claude --debug
   ```

## 常见模式

### 只读 Skill

```yaml
---
name: code-reader
description: 读取和分析代码而不进行更改。用于代码审查、理解代码库或文档。
allowed-tools: Read, Grep, Glob
---
```

### 基于脚本的 Skill

```yaml
---
name: data-processor
description: 使用 Python 脚本处理 CSV 和 JSON 数据文件。用于分析数据文件或转换数据集。
---

# Data Processor

## 说明

1. 使用处理脚本：
```bash
python scripts/process.py input.csv --output results.json
```

2. 使用以下命令验证输出：
```bash
python scripts/validate.py results.json
```
```

### 带渐进式披露的多文件 Skill

```yaml
---
name: api-designer
description: 遵循最佳实践设计 REST API。用于创建 API 端点、设计路由或规划 API 架构。
---

# API Designer

快速开始：参阅 [examples.md](examples.md)

详细参考：参阅 [reference.md](reference.md)

## 说明

1. 收集需求
2. 设计端点（参阅 examples.md）
3. 使用 OpenAPI 规范文档化
4. 根据最佳实践审查（参阅 reference.md）
```

## Skill 作者的最佳实践

1. **一个 Skill，一个目的**：不要创建 mega-Skills
2. **具体描述**：包含用户会说的触发词
3. **清晰说明**：为 Claude 而非人类写作
4. **具体示例**：显示真实代码，而非伪代码
5. **列出依赖项**：在描述中提及所需的包
6. **与团队成员测试**：验证激活和清晰度
7. **对你的 Skills 进行版本控制**：在内容中记录更改
8. **使用渐进式披露**：将高级细节放在单独的文件中

## 验证清单

在完成 Skill 之前，验证：

- [ ] 名称为小写、仅连字符，最多 64 个字符
- [ ] 描述具体且 < 1024 个字符
- [ ] 描述包含"什么"和"何时"
- [ ] YAML frontmatter 有效
- [ ] 说明是逐步的
- [ ] 示例具体且真实
- [ ] 依赖项已记录
- [ ] 文件路径使用正斜杠
- [ ] Skill 在相关查询时激活
- [ ] Claude 正确遵循说明

## 故障排除

**Skill 不激活**：
- 用触发词使描述更具体
- 在描述中包含文件类型和操作
- 添加"Use when..."子句与用户短语

**多个 Skills 冲突**：
- 使描述更具区别性
- 使用不同的触发词
- 缩小每个 Skills 的范围

**Skill 有错误**：
- 检查 YAML 语法（无制表符、正确的缩进）
- 验证文件路径（使用正斜杠）
- 确保脚本有执行权限
- 列出所有依赖项

## 示例

参阅文档获取完整示例：
- 简单的单文件 Skill（commit-helper）
- 带工具权限的 Skill（code-reviewer）
- 多文件 Skill（pdf-processing）

## 输出格式

在创建 Skill 时，我将：

1. 询问范围和需求的澄清问题
2. 建议 Skill 名称和位置
3. 使用正确的 frontmatter 创建 SKILL.md 文件
4. 包含清晰的说明和示例
5. 如需要，添加支持文件
6. 提供测试说明
7. 根据所有要求进行验证

结果将是一个完整的、可工作的 Skill，遵循所有最佳实践和验证规则。
