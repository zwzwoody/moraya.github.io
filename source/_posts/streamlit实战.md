---
title: Streamlit 实战：用 Python 构建 AI 驱动的 UI 自动化测试平台
date: 2026-02-17 13:53:51
tags:
  - Streamlit
  - Python
  - 自动化测试
  - AI测试
categories:
  - 技术实践
---
作为一名测试开发工程师，你是否也有这样的烦恼：写了一堆自动化测试用例，但每次执行都要在命令行里敲命令、改配置、翻日志？

如果你有这些困扰，那 Streamlit 可能是你的救星。它能让测试脚本秒变成友好的 Web 界面，让"点点点"替代"敲敲敲"。

这篇文章会带你完整走一遍：如何用 Streamlit 搭建一个 AI 驱动的 UI 自动化测试平台。过程中我会分享一些实战踩坑经验，帮你少走弯路。

{% asset_img 1771307370643.png %}

{% asset_img 1771307380918.png %}

---

## 目录

1. [先说说我们要做什么](#1-先说说我们要做什么)
2. [项目结构：为什么这么组织](#2-项目结构为什么这么组织)
3. [核心流程：页面是怎么跑起来的](#3-核心流程页面是怎么跑起来的)
4. [逐个模块拆解](#4-逐个模块拆解)
   - [入口文件：定好规矩再开工](#41-入口文件定好规矩再开工)
   - [状态管理：Streamlit 的灵魂](#42-状态管理streamlit-的灵魂)
   - [侧边栏：配置就该放边上](#43-侧边栏配置就该放边上)
   - [动态表单：最坑也最有价值](#44-动态表单最坑也最有价值)
   - [结果面板：让执行状态一目了然](#45-结果面板让执行状态一目了然)
   - [配置管理：数据总要存起来](#46-配置管理数据总要存起来)
   - [主页面：把积木拼起来](#47-主页面把积木拼起来)
5. [踩坑记录与最佳实践](#5-踩坑记录与最佳实践)

---

## 1. 先说说我们要做什么

这是一个 **Midscene UI 自动化测试平台**，核心能力是用自然语言驱动浏览器执行测试。比如你写一句"点击登录按钮，输入用户名和密码"，AI 就会自动理解并执行。

为了让测试人员用起来更方便，我们用 Streamlit 做了个可视化界面，主要实现这些功能：

- 可视化配置 AI 模型参数（不用改配置文件了）
- 用网页表单编写测试用例（不用写代码了）
- 一键执行、实时查看结果（不用切终端了）
- 多用例管理、分页展示（清爽不乱）

这些功能点看起来简单，但背后涉及 Streamlit 的几个核心概念：**多页面架构**、**Session State 状态管理**、**动态表单**、**非阻塞刷新**。下面我们逐个拆解。

---

## 2. 项目结构：为什么这么组织

先看目录结构：

```
streamlit/
├── streamlit_app.py          # 入口：定义页面路由
├── components/               # UI 组件（可复用的积木）
│   ├── state.py             # 状态初始化
│   ├── sidebar.py           # 侧边栏
│   ├── test_case_list.py   # 用例表单和列表
│   ├── result_panel.py     # 执行结果面板
│   └── dialogs.py          # 弹窗组件
├── pages/                   # 多个页面
│   ├── main_page.py        # 主页面（核心）
│   ├── page_2.py           # 扩展页面
│   └── page_3.py
├── executor/                # 测试执行引擎（与 Streamlit 解耦）
│   ├── executor.py         # Midscene 执行器
│   ├── ai_client.py        # AI 客户端
│   └── ...
├── utils/                   # 工具函数
│   └── config_manager.py   # 配置和用例的持久化
└── data/                    # 数据存储
    ├── midscene_config.json
    └── test_cases.json
```

**为什么要这么拆？**

| 目录            | 存什么       | 为什么单独放                               |
| --------------- | ------------ | ------------------------------------------ |
| `components/` | UI 组件函数  | 复用。侧边栏、表单这些在多个页面可能都用   |
| `pages/`      | 页面级别代码 | Streamlit 多页面机制要求，每个文件一个页面 |
| `executor/`   | 业务逻辑     | 解耦。执行测试的逻辑不应该和 UI 混在一起   |
| `utils/`      | 通用工具     | 配置读写、日志封装等，到处都要用           |
| `data/`       | JSON 文件    | 持久化存储，重启应用数据不丢               |

这个结构的核心思想是**职责分离**：UI 渲染、业务逻辑、数据存储各司其职，方便后续维护和扩展。

---

## 3. 核心流程：页面是怎么跑起来的

### 应用启动

```
streamlit run streamlit_app.py
         ↓
streamlit_app.py 定义了三个页面
         ↓
默认加载 main_page.py
         ↓
main_page.py 调用 init_session_state()
         ↓
初始化所有状态变量（配置、用例列表等）
         ↓
渲染侧边栏 + 主区域
```

### 用户操作流程

最典型的一个流程：用户添加并执行一个测试用例。

```
┌──────────────────┐      ┌───────────────────┐      ┌──────────────────┐
│ 填表单（用例名、  │      │ 点击"添加用例"    │      │ 保存到 JSON 文件 │
│ URL、步骤...）    │─────▶│                   │─────▶│                  │
└──────────────────┘      └───────────────────┘      └──────────────────┘

┌──────────────────┐      ┌───────────────────┐      ┌──────────────────┐
│ 点击"执行"按钮   │      │ 设置待执行标记    │      │ 后台执行器启动   │
│                  │─────▶│ pending_execute   │─────▶│ 页面每5秒刷新    │
└──────────────────┘      └───────────────────┘      └──────────────────┘
```

这里有个关键点：**执行测试是个耗时操作，不能让页面卡住**。所以我们用"设置标记 + 后台轮询"的方式，让执行器在后台跑，页面定时检查状态更新 UI。这就是后面要讲的 `st.fragment` 大法。

---

## 4. 逐个模块拆解

### 4.1 入口文件：定好规矩再开工

`streamlit_app.py` 是整个应用的入口，代码非常简洁：

```python
import streamlit as st

# 定义三个页面
main_page = st.Page("pages/main_page.py", title="Main Page", icon="🎈")
page_2 = st.Page("pages/page_2.py", title="Page 2", icon="❄️")
page_3 = st.Page("pages/page_3.py", title="Page 3", icon="🎉")

# 注册导航
pg = st.navigation([main_page, page_2, page_3])

# 启动！
pg.run()
```

**代码解读：**

- `st.Page(path, title, icon)`：定义一个页面，path 是页面脚本路径（相对于入口文件），title 和 icon 显示在导航栏
- `st.navigation([...])`：创建导航容器，传入所有页面
- `pg.run()`：启动应用，默认进入第一个页面

> 这里有个版本要求：`st.navigation` 是 Streamlit 1.37 引入的新 API，如果你用的是旧版本，需要升级一下：`pip install streamlit --upgrade`

入口文件保持简洁是好的实践。复杂逻辑都放到 `pages/` 和 `components/` 里，入口只负责"指路"。

---

### 4.2 状态管理：Streamlit 的灵魂

Streamlit 和传统 Web 框架最大的不同是：**它会在每次用户交互后重新执行整个脚本**。这意味着变量会重新初始化，想要"记住"状态，必须用 `st.session_state`。

看一下 `components/state.py`：

```python
import streamlit as st
from utils.config_manager import load_config, load_test_cases

def init_session_state():
    """初始化所有 session_state 变量"""

    # 典型的初始化模式：检查是否存在，不存在才初始化
    if "config_loaded" not in st.session_state:
        # 从本地 JSON 加载配置
        saved_config = load_config()
        st.session_state.midscene_config = saved_config["midscene_config"]
        st.session_state.headless_mode = saved_config.get("headless_mode", False)
        st.session_state.video_record = saved_config.get("video_record", True)
        st.session_state.config_loaded = True

    # 用例列表
    if "test_cases" not in st.session_state:
        st.session_state.test_cases = load_test_cases()

    # 执行结果存储
    if "execution_results" not in st.session_state:
        st.session_state.execution_results = {}

    # 待执行的用例（用于触发执行流程）
    if "pending_execute_case" not in st.session_state:
        st.session_state.pending_execute_case = None
```

**为什么这么写？**

因为 Streamlit 每次用户点击按钮、修改输入框，都会重新跑一遍脚本。如果直接写 `st.session_state.test_cases = load_test_cases()`，每次用户操作都会重新加载，之前编辑的内容就丢了。

用 `if "xxx" not in st.session_state` 判断，就能确保只在第一次加载时初始化。

**Session State 的增删改查：**

```python
# 读取
value = st.session_state.some_key
value = st.session_state.get("some_key", "默认值")  # 带默认值，不存在不报错

# 写入
st.session_state.some_key = "新值"

# 删除（很少用）
del st.session_state.some_key
```

---

### 4.3 侧边栏：配置就该放边上

侧边栏是放配置项的理想位置，不影响主区域的使用体验。

`components/sidebar.py` 的核心结构：

```python
import streamlit as st

def render_sidebar():
    """渲染侧边栏"""
    st.sidebar.title("配置")  # st.sidebar.xxx 都会显示在侧边栏

    _render_midscene_config()    # Midscene AI 配置
    _render_execution_options()  # 执行选项（无头模式等）
    _render_clear_button()       # 清空数据按钮
```

#### 只读/编辑模式切换

配置展示有两种状态：只读展示 vs 可编辑。这是个很实用的交互模式：

```python
def _render_midscene_config():
    """渲染 Midscene 配置区域"""
    config = st.session_state.midscene_config

    # 检查是否已配置完整
    is_configured = all([
        config.get("base_url"),
        config.get("api_key"),
        config.get("model_name"),
        config.get("model_family")
    ])

    # 用颜色标记配置状态
    if is_configured:
        st.sidebar.markdown("### Midscene 配置 :green[已配置]")
    else:
        st.sidebar.markdown("### Midscene 配置 :red[请配置]")

    # 根据编辑状态决定显示哪个版本
    if not st.session_state.midscene_editing:
        _render_config_readonly()  # 只读展示
    else:
        _render_config_edit()      # 可编辑表单
```

**这段代码的要点：**

1. `:green[xxx]` 是 Streamlit 的 Markdown 语法，可以给文字加颜色
2. 用一个状态变量 `midscene_editing` 控制显示模式
3. 避免每次渲染都弹出输入框，让界面更清爽

#### 编辑表单

```python
def _render_config_edit():
    """编辑模式的表单"""
    # 文本输入
    base_url = st.sidebar.text_input(
        "Base URL",
        value=st.session_state.midscene_config["base_url"],
        placeholder="https://your-api-endpoint.com"
    )

    # 密码输入（type="password" 会隐藏内容）
    api_key = st.sidebar.text_input(
        "API Key",
        type="password",  # 关键：敏感信息要隐藏
        value=st.session_state.midscene_config["api_key"],
        placeholder="sk-xxx"
    )

    model_name = st.sidebar.text_input(
        "模型名称",
        value=st.session_state.midscene_config["model_name"]
    )

    model_family = st.sidebar.selectbox(
        "模型类型",
        options=["openai", "anthropic", "custom"],
        index=["openai", "anthropic", "custom"].index(
            st.session_state.midscene_config.get("model_family", "openai")
        )
    )

    # 保存和取消按钮
    col_save, col_cancel = st.sidebar.columns(2)
    with col_save:
        if st.button("保存", key="save_config", type="primary"):
            # 更新配置
            st.session_state.midscene_config = {
                "base_url": base_url,
                "api_key": api_key,
                "model_name": model_name,
                "model_family": model_family
            }
            save_config({"midscene_config": st.session_state.midscene_config})
            st.session_state.midscene_editing = False
            st.rerun()  # 刷新页面，更新显示
    with col_cancel:
        if st.button("取消", key="cancel_config"):
            st.session_state.midscene_editing = False
            st.rerun()
```

**要点：**

- `type="password"`：API Key 这种敏感信息，必须隐藏
- `st.columns(2)`：两个按钮并排显示
- `st.rerun()`：保存后立即刷新页面，让用户看到最新状态

#### 复选框 + 自动保存

```python
def _render_execution_options():
    """执行选项"""
    st.sidebar.markdown("### 执行选项")

    # 定义回调：选项变化时自动保存
    def on_option_change():
        save_config({
            "midscene_config": st.session_state.midscene_config,
            "headless_mode": st.session_state.headless_mode,
            "video_record": st.session_state.video_record
        })

    st.sidebar.checkbox(
        "无头模式（不显示浏览器）",
        value=st.session_state.get("headless_mode", False),
        key="headless_mode",
        on_change=on_option_change  # 变化时触发回调
    )

    st.sidebar.checkbox(
        "录制视频",
        value=st.session_state.get("video_record", True),
        key="video_record",
        on_change=on_option_change
    )
```

`on_change` 是 Streamlit 的回调机制：当组件值变化时自动调用指定函数。比"点按钮保存"更流畅。

---

### 4.4 动态表单：最坑也最有价值

这是整个项目最复杂的部分：一个可以动态增删步骤的表单。

**为什么说它坑？** 因为 Streamlit 的 widget 和 session_state 有特殊的绑定机制，直接修改状态不会立刻反映到 widget 上，必须用"延迟赋值"模式。

#### 延迟赋值模式

```python
def render_test_case_form():
    """渲染测试用例表单"""

    # ===== 第一步：声明所有表单字段的状态变量 =====
    if "form_test_name" not in st.session_state:
        st.session_state.form_test_name = ""
    if "form_initial_url" not in st.session_state:
        st.session_state.form_initial_url = ""
    if "form_steps" not in st.session_state:
        st.session_state.form_steps = [{"id": 1}]  # 初始一个步骤
    if "_step_id_counter" not in st.session_state:
        st.session_state._step_id_counter = 2  # 用于生成唯一 ID

    # ===== 第二步：在 widget 创建前处理待执行的操作 =====
    # 关键！一定要在 widget 实例化之前处理
    if st.session_state.get("_pending_edit_case"):
        # 编辑用例：填充表单
        _fill_form_fields(st.session_state._pending_edit_case)
        st.session_state._pending_edit_case = None
    elif st.session_state.get("_pending_clear_form"):
        # 清空表单
        _clear_form_fields()
        st.session_state._pending_clear_form = False

    # ===== 第三步：渲染 widget =====
    # 这时 widget 会读取 session_state 里的值
    test_name = st.text_input("用例名称", key="form_test_name")
    initial_url = st.text_input("初始URL", key="form_initial_url")

    # ... 渲染步骤 ...
```

这个模式的精髓是：**不要直接修改 widget 的 value**，而是修改绑定的 session_state，然后刷新页面让 widget 重新读取。

#### 动态步骤渲染

```python
# 步骤区域的表头
col_h_idx, col_h_action, col_h_task, col_h_del = st.columns([0.5, 2, 6, 0.8])
with col_h_action:
    st.caption("操作类型")
with col_h_task:
    st.caption("任务描述")

# 遍历渲染每个步骤
action_options = ["ai", "switch_domain", "query", "verify"]
for i, step in enumerate(st.session_state.form_steps):
    sid = step["id"]  # 每个步骤有唯一 ID

    col_idx, col_action, col_task, col_del = st.columns([0.5, 2, 6, 0.8])

    with col_idx:
        st.markdown(f"{i + 1}.")  # 序号

    with col_action:
        # 操作类型选择
        st.selectbox(
            f"action_{sid}",
            options=action_options,
            key=f"step_action_{sid}",  # 动态 key，避免冲突
            label_visibility="collapsed"
        )

    with col_task:
        # 根据操作类型显示不同的输入组件
        current_action = st.session_state.get(f"step_action_{sid}", "ai")
        if current_action == "switch_domain":
            # 切换登录态：显示下拉选择
            st.selectbox(
                f"domain_{sid}",
                options=["admin", "user", "h5"],
                key=f"step_domain_{sid}",
                label_visibility="collapsed"
            )
        else:
            # 其他操作：显示文本输入
            st.text_input(
                f"task_{sid}",
                key=f"step_task_{sid}",
                placeholder="用自然语言描述操作...",
                label_visibility="collapsed"
            )

    with col_del:
        # 删除按钮（至少保留一个步骤）
        if len(st.session_state.form_steps) > 1:
            if st.button("删除", key=f"del_{sid}"):
                st.session_state.form_steps = [
                    s for s in st.session_state.form_steps if s["id"] != sid
                ]
                st.rerun()

# 添加步骤按钮
if st.button("添加步骤"):
    new_id = st.session_state._step_id_counter
    st.session_state._step_id_counter += 1
    st.session_state.form_steps.append({"id": new_id})
    st.rerun()
```

**关键点：**

1. **动态 key**：每个 widget 用 `f"step_action_{sid}"` 这种动态 key，避免多个组件 key 冲突
2. **条件渲染**：根据 step 的 action 类型，渲染不同的输入组件
3. **列表操作**：增删步骤本质是操作 `st.session_state.form_steps` 列表

#### 提交处理

```python
if st.button("添加用例", type="primary"):
    # 收集步骤数据
    steps = []
    for step in st.session_state.form_steps:
        sid = step["id"]
        action = st.session_state.get(f"step_action_{sid}", "ai")
        if action == "switch_domain":
            task = st.session_state.get(f"step_domain_{sid}", "admin")
        else:
            task = st.session_state.get(f"step_task_{sid}", "").strip()

        if task:  # 空步骤不加入
            steps.append({"action": action, "task": task})

    # 验证必填项
    errors = []
    if not test_name.strip():
        errors.append("用例名称")
    if not initial_url.strip():
        errors.append("初始URL")
    if not steps:
        errors.append("至少一个有效步骤")

    if errors:
        st.toast(f"请填写：{', '.join(errors)}", icon="!")
    else:
        # 构建用例对象
        new_case = {
            "id": str(int(time.time())),
            "name": test_name.strip(),
            "initial_url": initial_url.strip(),
            "steps": steps,
            "status": "待执行",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        # 保存
        st.session_state.test_cases.append(new_case)
        save_test_cases(st.session_state.test_cases)

        # 清空表单（通过标记，下次渲染时处理）
        st.session_state._pending_clear_form = True
        st.toast("添加成功！", icon="✅")
        st.rerun()
```

#### 分页显示

用例多了要分页，不然页面会无限长：

```python
ITEMS_PER_PAGE = 5

def render_test_case_list():
    """渲染用例列表（分页）"""
    if not st.session_state.test_cases:
        st.info("暂无用例，去添加一个吧~")
        return

    # 计算分页
    total = len(st.session_state.test_cases)
    total_pages = (total + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    # 确保当前页有效
    current = st.session_state.current_page
    current = max(0, min(current, total_pages - 1))
    st.session_state.current_page = current

    # 当前页数据（最新的在前面）
    start = current * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_cases = list(reversed(st.session_state.test_cases))[start:end]

    # 渲染每个用例
    for case in page_cases:
        _render_case_item(case)

    # 分页控件
    col_prev, col_info, col_next = st.columns([1, 2, 1])
    with col_prev:
        if st.button("上一页", disabled=current == 0):
            st.session_state.current_page -= 1
            st.rerun()
    with col_info:
        st.markdown(f"<center>第 {current + 1} / {total_pages} 页</center>", unsafe_allow_html=True)
    with col_next:
        if st.button("下一页", disabled=current >= total_pages - 1):
            st.session_state.current_page += 1
            st.rerun()
```

---

### 4.5 结果面板：让执行状态一目了然

`components/result_panel.py` 负责显示执行结果和统计。

#### 弹窗对话框

Streamlit 1.30+ 支持 `@st.dialog` 装饰器，实现模态弹窗：

```python
@st.dialog("使用说明", width="large")
def show_help_dialog():
    """帮助弹窗"""
    st.markdown("""
    ### 快速开始

    1. 左侧配置 AI 模型参数
    2. 填写测试用例信息
    3. 点击执行，观察结果

    ### 操作类型说明

    - **AI 分析**：让 AI 自由操作（不推荐用于关键流程）
    - **执行操作**：按自然语言描述执行动作
    - **切换登录态**：切换到不同的账号登录态
    - **查询**：只读操作，获取页面数据
    - **验证**：断言检查
    """)
    if st.button("我知道了", type="primary"):
        st.rerun()  # 关闭弹窗

# 在主流程中调用
if st.button("帮助"):
    show_help_dialog()
```

#### 指标展示

```python
def render_statistics():
    """统计数据"""
    cases = st.session_state.test_cases
    total = len(cases)
    success = sum(1 for c in cases if c["status"] == "成功")
    failed = sum(1 for c in cases if c["status"] == "失败")
    running = sum(1 for c in cases if c["status"] == "执行中...")

    # 单个大指标
    st.metric("总用例数", total)

    # 多列指标
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("成功", success, delta=f"{success/total*100:.1f}%" if total else "0%")
    with col2:
        st.metric("失败", failed, delta_color="inverse")
    with col3:
        st.metric("执行中", running)
```

`st.metric` 会自动显示一个加粗的大数字，适合展示关键指标。

---

### 4.6 配置管理：数据总要存起来

`utils/config_manager.py` 负责 JSON 文件的读写。

```python
import os
import json

# 获取 data 目录路径
_STREAMLIT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(_STREAMLIT_DIR, "data")

CONFIG_FILE = os.path.join(DATA_DIR, "midscene_config.json")
CASES_FILE = os.path.join(DATA_DIR, "test_cases.json")

def ensure_data_dir():
    """确保数据目录存在"""
    os.makedirs(DATA_DIR, exist_ok=True)

def load_config():
    """加载配置"""
    default = {
        "midscene_config": {
            "base_url": "",
            "api_key": "",
            "model_name": "",
            "model_family": ""
        },
        "headless_mode": False,
        "video_record": True
    }

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                # 合并默认值（处理新增字段）
                for key in default:
                    if key not in saved:
                        saved[key] = default[key]
                return saved
        except (json.JSONDecodeError, IOError):
            return default
    return default

def save_config(config):
    """保存配置"""
    ensure_data_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
```

**几个细节：**

1. `os.makedirs(exist_ok=True)`：目录不存在就创建，存在也不报错
2. `encoding="utf-8"`：处理中文必须指定编码
3. 合并默认值：配置文件可能是旧版本，新字段缺失时用默认值填充

---

### 4.7 主页面：把积木拼起来

`pages/main_page.py` 是各个组件的组装点。

#### 页面配置

```python
import streamlit as st
from datetime import timedelta

# 导入组件
from components.state import init_session_state
from components.sidebar import render_sidebar
from components.test_case_list import render_test_case_form, render_test_case_list
from components.result_panel import render_result_panel

# 页面配置——必须在最前面
st.set_page_config(
    page_title="Midscene UI 自动化测试",
    layout="wide",  # 宽屏布局，利用更多空间
    page_icon="🤖"
)

# 初始化状态
init_session_state()
```

`st.set_page_config` 必须在所有 Streamlit 命令之前调用，否则报错。

#### 分段控制器（Segmented Control）

这是 Streamlit 1.38 新增的组件，类似 tab 但更灵活：

```python
tabs = ["用例编辑", "用例列表"]
active = st.segmented_control(
    "功能区",
    options=tabs,
    key="_active_tab",
    label_visibility="collapsed"
)

if active == "用例编辑":
    render_test_case_form()
else:
    render_test_case_list()
```

#### 非阻塞自动刷新

这是解决"执行测试时页面卡死"的关键：

```python
@st.fragment(run_every=timedelta(seconds=5))
def monitor_execution():
    """后台监控执行状态，每 5 秒刷新"""
    running = sum(1 for c in st.session_state.test_cases if c["status"] == "执行中...")

    if running > 0:
        st.caption(f"有 {running} 个用例正在执行...")

    # 之前有执行中的，现在都完成了，触发全页面刷新
    prev = st.session_state.get("_prev_running", 0)
    if prev > 0 and running == 0:
        st.rerun(scope="app")

    st.session_state._prev_running = running

# 调用
monitor_execution()
```

**`@st.fragment` 的妙处：**

普通 `st.rerun()` 会重新执行整个脚本，用户在填表单时体验很差。`st.fragment` 创建一个独立刷新区域，只有这个区域会定时刷新，不影响用户的其他操作。

---

## 5. 踩坑记录与最佳实践

### 踩坑 1：Widget key 冲突

**现象：** 表单显示异常，或者报错 "Duplicate widget ID"

**原因：** 动态生成的 widget 使用了相同的 key

**解决：** 用唯一 ID 拼接 key

```python
# 错误
st.text_input("步骤", key="step")  # 所有步骤都叫 step

# 正确
st.text_input("步骤", key=f"step_{step_id}")  # step_1, step_2, ...
```

### 踩坑 2：状态不同步

**现象：** 修改了 session_state，页面没变化

**原因：** Streamlit 需要手动触发刷新

**解决：** `st.rerun()`

```python
if st.button("删除"):
    st.session_state.items.remove(item)
    st.rerun()  # 必须调用，否则页面不更新
```

### 踩坑 3：动态表单值无法更新

**现象：** 点击"编辑用例"后，表单显示的还是旧值

**原因：** 直接修改了 session_state，但 widget 已经缓存了旧值

**解决：** 使用"延迟赋值"模式——设置标记，下次渲染时处理

```python
# 点击编辑按钮时
if st.button("编辑"):
    st.session_state._pending_edit = case_data  # 只设置标记
    st.rerun()

# 在 widget 渲染前处理
if st.session_state.get("_pending_edit"):
    _fill_form(st.session_state._pending_edit)
    st.session_state._pending_edit = None
```

### 最佳实践总结

| 方面       | 建议                                                 |
| ---------- | ---------------------------------------------------- |
| 状态初始化 | 用 `if key not in session_state`，避免覆盖用户输入 |
| 组件设计   | 每个函数只渲染一个区域，单一职责                     |
| 用户反馈   | 用 `st.toast()` 提示操作结果                       |
| 防重复提交 | 按钮在执行时禁用                                     |
| 大列表     | 必须分页                                             |
| 长操作     | 用 fragment 或后台任务，避免页面卡死                 |
| 文件编码   | 始终 `encoding="utf-8"`                            |

---

## 附录：Streamlit 常用 API 速查

### 输入组件

| API                 | 用途     | 常用参数                             |
| ------------------- | -------- | ------------------------------------ |
| `st.text_input()` | 单行文本 | `placeholder`, `type="password"` |
| `st.text_area()`  | 多行文本 | `height`                           |
| `st.selectbox()`  | 下拉选择 | `options`, `format_func`         |
| `st.checkbox()`   | 复选框   | `value`, `on_change`             |
| `st.button()`     | 按钮     | `type="primary"`, `disabled`     |

### 显示组件

| API                | 用途          |
| ------------------ | ------------- |
| `st.markdown()`  | Markdown 内容 |
| `st.metric()`    | 指标卡片      |
| `st.dataframe()` | 可交互表格    |
| `st.code()`      | 代码高亮      |
| `st.toast()`     | 提示消息      |

### 布局组件

| API                | 用途     |
| ------------------ | -------- |
| `st.columns()`   | 多列布局 |
| `st.tabs()`      | 标签页   |
| `st.sidebar`     | 侧边栏   |
| `st.container()` | 逻辑容器 |

### 高级功能

| API                  | 用途         |
| -------------------- | ------------ |
| `st.fragment()`    | 局部刷新区域 |
| `st.dialog()`      | 弹窗         |
| `st.rerun()`       | 页面刷新     |
| `st.session_state` | 状态管理     |

---

> 本文基于 Streamlit 1.38+ 版本，部分 API（如 `st.fragment`、`st.segmented_control`）需要较新版本。升级命令：`pip install streamlit --upgrade`
