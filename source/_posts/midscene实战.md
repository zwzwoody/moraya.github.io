---
title: Midscene 实战：当 AI 遇上自动化测试
date: 2026-02-17 17:13:03
tags:
  - Midscene
  - AI测试
  - 自动化测试
  - Selenium
categories:
  - 技术实践
---
## 写在前面

作为一名测试工程师，你是否也经历过这样的痛苦：

- 页面元素改了个 class 名，测试脚本全线崩溃
- 写了半天的 XPath 选择器，运行时却找不到元素

如果这些场景让你感同身受，那么今天要介绍的 **Midscene** 可能会让你眼前一亮——它是一个 AI 驱动的 Web 自动化测试框架，能够用自然语言来操作浏览器，告别繁琐的选择器维护。

## 什么是 Midscene？

Midscene是字节跳动开源的基于AI的UI自动化框架，简单来说，Midscene 是一个让 AI 帮你"看"网页并执行操作的测试框架。传统的自动化测试需要精确定位元素（比如 `//div[@class="submit-btn"]`），而 Midscene 只需要告诉它"点击提交按钮"，AI 就能理解并执行。

### 核心优势

1. **自然语言驱动**：用中文描述操作意图，AI 自动理解执行
2. **自动失败恢复**：Selenium 测试失败时，AI 自动接手重试
3. **无选择器维护**：不需要写 XPath、CSS 选择器，页面改版影响小
4. **与现有框架兼容**：可以在现有 Selenium + Pytest 基础上增强

## 项目架构一览

先来看一下整体架构：

```
┌─────────────────────────────────────────────────────────────┐
│                      Jenkins Pipeline                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│           Midscene Bridge (Node.js 服务，端口 3000)          │
│  • 接收 Python 发来的 AI 操作请求                             │
│  • 通过 CDP 协议连接 Chrome 浏览器                            │
│  • 调用 @midscene/playwright 执行 AI 操作                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Chrome 浏览器 (CDP 端口 9222)                   │
│  • 被 Selenium 和 AI 共同控制                                │
│  • Selenium 先执行传统操作                                    │
│  • 失败时 AI 通过 CDP 接管                                    │
└─────────────────────────────────────────────────────────────┘
```

这个架构的精妙之处在于：**Selenium 和 AI 共享同一个浏览器实例**。当传统的 Selenium 操作失败时，AI 可以无缝接手，尝试用"智能"的方式完成任务。

## 四大核心方法

Midscene 提供了四个主要的 AI 操作方法，覆盖日常测试的各种场景：

### 1. ai_do - 执行操作

当你需要点击、输入、滚动等操作时使用：

```python
# 传统方式：先找元素，再操作
driver.find_element(By.XPATH, "//button[contains(text(),'登录')]").click()

# Midscene 方式：直接说你要做什么
midscene.ai_do("点击登录按钮")
midscene.ai_do("在用户名输入框输入 'admin'")
midscene.ai_do("滚动到页面底部")
```

**适用场景**：按钮点击、表单填写、页面滚动、菜单展开等操作类动作。

### 2. ai_query - 查询信息

当你需要从页面上获取一些信息时使用：

```python
# 传统方式：定位元素，获取文本
element = driver.find_element(By.CLASS_NAME, "username")
username = element.text

# Midscene 方式：直接问你想知道什么
username = midscene.ai_query("当前登录的用户名是什么？")
price = midscene.ai_query("商品价格是多少？")
count = midscene.ai_query("购物车里有几件商品？")
```

**适用场景**：获取页面文本、数值、状态等信息。

### 3. ai_assert - 断言验证

当你需要验证页面状态是否符合预期时使用：

```python
# 传统方式：获取元素，断言
element = driver.find_element(By.XPATH, "//*[contains(text(),'成功')]")
assert element.is_displayed()

# Midscene 方式：用自然语言描述预期
midscene.ai_assert("页面是否显示'操作成功'")
midscene.ai_assert("登录按钮是否可用")
midscene.ai_assert("购物车数量是否大于0")
```

**适用场景**：断言页面元素是否存在、状态是否正确、数值是否符合预期。

### 4. ai_plan - 自动规划

这是一个更高级的方法，AI 会自动规划并执行多步操作：

```python
# 传统方式：需要写多个操作步骤
driver.find_element(By.ID, "username").send_keys("admin")
driver.find_element(By.ID, "password").send_keys("123456")
driver.find_element(By.CLASS_NAME, "login-btn").click()
assert "欢迎" in driver.page_source

# Midscene 方式：一句话搞定
midscene.ai_plan("完成登录并验证登录成功")
```

**适用场景**：复杂的任务流程，让 AI 自动拆解步骤执行。

## 实战：从零开始集成 Midscene

### 第一步：启动 Midscene 服务

Midscene 的核心是一个 Node.js 服务，负责处理 AI 请求。我们封装了一个 Python 类来自动管理这个服务：

```python
# common/midscene_service.py

import subprocess
import time
import requests
import os

class MidsceneService:
    """
    Midscene 服务管理器

    主要功能：
    1. 自动启动 Node.js 服务
    2. 健康检查确保服务可用
    3. 进程管理（启动/停止/状态查询）
    """

    def __init__(self, bridge_path: str, port: int = 3000):
        """
        初始化服务管理器

        Args:
            bridge_path: midscene-bridge 目录的路径
            port: 服务监听端口，默认 3000
        """
        self.bridge_path = bridge_path
        self.port = port
        self.process = None
        self.base_url = f"http://localhost:{port}"

    def start(self) -> bool:
        """
        启动 Midscene 服务

        Returns:
            bool: 启动是否成功
        """
        # 检查服务是否已经在运行
        if self.is_healthy():
            print(f"Midscene 服务已在端口 {self.port} 运行")
            return True

        # 检查 npm 依赖是否安装
        node_modules = os.path.join(self.bridge_path, "node_modules")
        if not os.path.exists(node_modules):
            print("正在安装 npm 依赖...")
            subprocess.run(["npm", "install"], cwd=self.bridge_path, shell=True)

        # 启动 Node.js 服务
        print(f"正在启动 Midscene 服务 (端口 {self.port})...")
        self.process = subprocess.Popen(
            ["node", "server.js"],
            cwd=self.bridge_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # 等待服务就绪
        return self._wait_for_healthy()

    def is_healthy(self) -> bool:
        """
        检查服务健康状态

        通过调用 /health 端点确认服务正常响应

        Returns:
            bool: 服务是否健康
        """
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

    def _wait_for_healthy(self, timeout: int = 30) -> bool:
        """
        等待服务变为健康状态

        Args:
            timeout: 超时时间（秒）

        Returns:
            bool: 服务是否在超时前变为健康
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_healthy():
                print("Midscene 服务启动成功")
                return True
            time.sleep(1)

        print("Midscene 服务启动超时")
        return False

    def stop(self):
        """停止服务"""
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("Midscene 服务已停止")
```

**为什么需要这个服务管理器？**

因为 Midscene 目前没有官方 Python SDK，我们需要通过 Node.js 服务来桥接。这个管理器的作用：

1. **自动化**：测试开始时自动启动服务，无需手动干预
2. **健壮性**：健康检查确保服务真正可用后才继续
3. **便捷性**：封装了 npm 安装、进程管理等复杂操作

### 第二步：编写 AI 操作助手

有了服务，我们还需要一个助手类来发送 AI 操作请求：

```python
# common/midscene_helper.py

import requests
import time
from typing import Optional, Any

class MidsceneHelper:
    """
    Midscene AI 操作助手

    封装了与 Midscene Bridge 的通信逻辑，
    提供简洁的 API 供测试用例使用
    """

    def __init__(self, base_url: str = "http://localhost:3000",
                 cdp_endpoint: str = "http://localhost:9222"):
        """
        初始化助手

        Args:
            base_url: Midscene Bridge 服务地址
            cdp_endpoint: Chrome DevTools Protocol 端点
                         （Selenium 启动 Chrome 时需开启远程调试）
        """
        self.base_url = base_url
        self.cdp_endpoint = cdp_endpoint
        self.timeout = 60  # AI 操作超时时间

    def ai_do(self, action: str, context: str = "") -> bool:
        """
        执行一个 AI 操作

        Args:
            action: 操作描述，如 "点击登录按钮"
            context: 额外上下文信息（可选）

        Returns:
            bool: 操作是否成功

        Example:
            >>> midscene.ai_do("点击用户菜单中的'退出'按钮")
            True
        """
        payload = {
            "action": "do",
            "prompt": action,
            "cdpEndpoint": self.cdp_endpoint,
            "context": context
        }

        result = self._send_request(payload)
        return result.get("success", False)

    def ai_query(self, query: str) -> Optional[Any]:
        """
        查询页面信息

        Args:
            query: 查询问题，如 "当前页面标题是什么"

        Returns:
            查询结果，类型取决于问题

        Example:
            >>> username = midscene.ai_query("用户名输入框的值是什么")
            "admin"
        """
        payload = {
            "action": "query",
            "prompt": query,
            "cdpEndpoint": self.cdp_endpoint
        }

        result = self._send_request(payload)
        return result.get("data")

    def ai_assert(self, assertion: str) -> bool:
        """
        AI 断言

        Args:
            assertion: 断言描述，如 "登录按钮是否可见"

        Returns:
            bool: 断言是否成立

        Example:
            >>> midscene.ai_assert("页面是否显示'操作成功'提示")
            True
        """
        payload = {
            "action": "assert",
            "prompt": assertion,
            "cdpEndpoint": self.cdp_endpoint
        }

        result = self._send_request(payload)
        return result.get("success", False)

    def ai_plan(self, task: str) -> bool:
        """
        AI 自动规划并执行任务

        Args:
            task: 任务描述，如 "完成登录流程"

        Returns:
            bool: 任务是否成功完成

        Example:
            >>> midscene.ai_plan("登录并进入个人中心")
            True
        """
        payload = {
            "action": "ai",
            "prompt": task,
            "cdpEndpoint": self.cdp_endpoint
        }

        result = self._send_request(payload)
        return result.get("success", False)

    def _send_request(self, payload: dict) -> dict:
        """
        发送请求到 Midscene Bridge

        Args:
            payload: 请求体

        Returns:
            dict: 响应结果
        """
        try:
            response = requests.post(
                f"{self.base_url}/ai-action",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            return {"success": False, "error": "请求超时"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
```

**这段代码的设计思路：**

1. **单一职责**：每个方法只做一件事，便于理解和维护
2. **类型提示**：使用 Python 类型注解，IDE 支持更好
3. **错误处理**：网络异常、超时等情况都有处理
4. **文档友好**：每个方法都有详细的 docstring 和示例

### 第三步：Node.js 服务端实现

Python 端准备好了，接下来是 Node.js 服务端。这个服务负责接收请求并调用 Midscene AI：

```javascript
// midscene/midscene-bridge/server.js

const express = require('express');
const { chromium } = require('@midscene/playwright');

const app = express();
app.use(express.json());

// AI 模型配置
// 这里使用 OpenAI 兼容的 API 接口
process.env.OPENAI_API_KEY = 'your-api-key';
process.env.OPENAI_BASE_URL = 'https://api.openai.com/v1';

/**
 * 健康检查端点
 * 用于确认服务正常运行
 */
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

/**
 * AI 操作端点
 * 接收来自 Python 的 AI 操作请求
 */
app.post('/ai-action', async (req, res) => {
  const { action, prompt, cdpEndpoint, context } = req.body;

  console.log(`收到 AI 操作请求: action=${action}, prompt=${prompt}`);

  try {
    // 通过 CDP 连接到已有的 Chrome 浏览器
    // 这样可以共享 Selenium 已经打开的浏览器会话
    const browser = await chromium.connectOverCDP(cdpEndpoint);
    const context = browser.contexts()[0];
    const page = context.pages()[0];

    let result;

    // 根据操作类型调用对应的 Midscene API
    switch (action) {
      case 'do':
        // 执行操作：点击、输入、滚动等
        await page.aiDo(prompt);
        result = { success: true, message: `已执行: ${prompt}` };
        break;

      case 'query':
        // 查询信息：获取页面上的文本、数值等
        const data = await page.aiQuery(prompt);
        result = { success: true, data: data };
        break;

      case 'assert':
        // 断言验证：检查页面状态
        const assertResult = await page.aiAssert(prompt);
        result = { success: assertResult, message: `断言结果: ${assertResult}` };
        break;

      case 'ai':
        // 自动规划：AI 自己决定如何完成任务
        await page.aiAction(prompt);
        result = { success: true, message: `任务完成: ${prompt}` };
        break;

      default:
        result = { success: false, error: `未知操作类型: ${action}` };
    }

    // 不关闭 browser，因为要共享浏览器会话
    res.json(result);

  } catch (error) {
    console.error('AI 操作失败:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Midscene Bridge 服务已启动，端口: ${PORT}`);
  console.log(`健康检查: http://localhost:${PORT}/health`);
});
```

**关键点解释：**

1. **CDP 连接**：`chromium.connectOverCDP()` 让我们可以连接到已存在的 Chrome 实例，这是实现 Selenium 和 AI 共享浏览器的关键。
2. **操作分发**：根据 action 类型调用不同的 Midscene API，清晰明了。
3. **会话保持**：操作完成后不关闭 browser，保持浏览器会话，让后续操作可以继续。

### 第四步：写一个真实的测试用例

配置都准备好了，来看一个完整的测试用例：

```python
# test_case/test_midscene/test_sign_in.py

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from common.midscene_helper import MidsceneHelper

class TestSignIn:
    """签到功能测试 - AI 增强版"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """测试初始化：启动浏览器和 AI 助手"""
        # 配置 Chrome，开启远程调试端口
        # 这个端口让 AI 可以连接并控制浏览器
        chrome_options = Options()
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument('--start-maximized')

        self.driver = webdriver.Chrome(options=chrome_options)
        self.midscene = MidsceneHelper(
            cdp_endpoint="http://localhost:9222"
        )

        yield

        self.driver.quit()

    def test_sign_in_flow(self):
        """
        测试签到流程

        业务场景：
        1. 用户进入签到页面
        2. 点击签到按钮
        3. 验证签到成功提示

        这个用例演示了传统 Selenium 和 AI 操作的混合使用
        """
        # ========== 第一步：使用传统方式导航到签到页面 ==========
        # 导航类操作用传统方式更稳定可控
        self.driver.get("https://example.com/sign-in")

        # ========== 第二步：使用 AI 完成签到 ==========
        # 为什么这里用 AI？
        # - 签到按钮的位置、样式可能经常变化
        # - 不同日期可能显示不同的签到状态
        # - AI 能理解"签到"这个意图，自动找到正确的按钮

        success = self.midscene.ai_do("点击签到按钮")
        assert success, "签到操作失败"

        # ========== 第三步：使用 AI 验证签到结果 ==========
        # 为什么这里用 AI 断言？
        # - 成功提示的文案、位置、样式可能变化
        # - 用 AI 断言只需要描述"预期是什么"

        assert self.midscene.ai_assert("是否显示签到成功"), \
            "未显示签到成功提示"

        # ========== 第四步：用 AI 查询验证数据 ==========
        # 查询连续签到天数
        consecutive_days = self.midscene.ai_query(
            "连续签到天数是多少"
        )
        print(f"连续签到: {consecutive_days} 天")

        # 可以结合传统断言做精确验证
        assert int(consecutive_days) >= 1, "签到天数应该 >= 1"

    def test_sign_in_with_rewards(self):
        """
        测试签到奖励场景

        这个用例使用 ai_plan 让 AI 自动规划执行
        适合较复杂的业务流程
        """
        self.driver.get("https://example.com/sign-in")

        # 一句话让 AI 完成整个签到领奖励流程
        # AI 会自动：
        # 1. 查找签到按钮
        # 2. 点击签到
        # 3. 识别弹出的奖励弹窗
        # 4. 点击领取奖励
        # 5. 关闭弹窗
        success = self.midscene.ai_plan(
            "完成签到并领取签到奖励"
        )

        assert success, "签到领奖励流程失败"

        # 验证奖励是否到账
        points = self.midscene.ai_query("当前积分余额")
        print(f"当前积分: {points}")
```

**从代码中我们可以学到：**

1. **混合使用**：不是所有操作都要用 AI，导航、等待等操作用传统方式更可控
2. **扬长避短**：让 AI 处理易变的 UI 元素，传统方式处理稳定的操作
3. **渐进式采用**：可以在现有测试基础上逐步引入 AI，不必重写

## 高级特性：自动失败恢复

Midscene 最实用的特性是"自动失败恢复"。当 Selenium 测试失败时，AI 自动接管重试：

```python
# conftest.py

import pytest
from common.midscene_helper import MidsceneHelper

# 注册自定义标记
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "ai_task(task_description): AI 自动恢复任务描述"
    )

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    测试失败时自动触发 AI 重试

    流程：
    1. 测试执行失败
    2. 检查是否有 @pytest.mark.ai_task 标记
    3. 如果有，调用 Midscene AI 尝试完成任务
    4. 在 Allure 报告中记录 AI 重试结果
    """
    outcome = yield
    report = outcome.get_result()

    # 只在测试失败且是调用阶段时处理
    if report.failed and call.when == "call":
        # 检查是否有 AI 任务标记
        ai_task_marker = item.get_closest_marker("ai_task")

        if ai_task_marker:
            task_description = ai_task_marker.args[0]
            print(f"\n测试失败，启动 AI 重试: {task_description}")

            try:
                midscene = MidsceneHelper()
                success = midscene.ai_plan(task_description)

                if success:
                    # AI 重试成功，修改测试结果
                    report.outcome = 'passed'
                    report.wasxfail = "AI 自动恢复成功"

                    # 记录到 Allure 报告
                    if hasattr(item, '_allure_label'):
                        item._allure_label = "AI-Retry-Success"
                else:
                    # AI 重试失败
                    if hasattr(item, '_allure_label'):
                        item._allure_label = "AI-Retry-Failed"

            except Exception as e:
                print(f"AI 重试异常: {e}")
```

**使用方式非常简单：**

```python
import pytest

class TestOrder:
    """订单测试"""

    @pytest.mark.ai_task("完成下单流程")
    def test_create_order(self, driver):
        """
        测试创建订单

        如果传统 Selenium 操作失败，
        AI 会自动尝试"完成下单流程"
        """
        driver.get("https://example.com/order")

        # 传统方式操作
        driver.find_element(By.ID, "product").click()
        driver.find_element(By.CLASS_NAME, "buy-now").click()

        # 如果这里失败了，AI 会接手
        driver.find_element(By.XPATH, "//button[text()='提交订单']").click()
```

**自动失败恢复的价值：**

1. **减少误报**：偶发性失败自动恢复，减少无效的 bug 报告
2. **提高稳定性**：页面元素变化时，AI 能自动适应
3. **降低维护成本**：不用为每个选择器变化修改代码

## Jenkins 流水线集成

最后，来看看如何在 CI/CD 中使用：

```groovy
// Jenkinsfile.midscene

pipeline {
    agent any

    environment {
        MIDSCENE_PORT = '3000'
        CHROME_CDP_PORT = '9222'
    }

    stages {
        stage('环境准备') {
            steps {
                sh '''
                    # 检查 Node.js 环境
                    node --version
                    npm --version

                    # 安装 Midscene Bridge 依赖
                    cd midscene/midscene-bridge
                    npm install
                '''
            }
        }

        stage('启动 Midscene 服务') {
            steps {
                sh '''
                    cd midscene/midscene-bridge
                    nohup node server.js > midscene.log 2>&1 &

                    # 等待服务就绪
                    for i in {1..30}; do
                        if curl -s http://localhost:3000/health; then
                            echo "Midscene 服务已就绪"
                            break
                        fi
                        sleep 1
                    done
                '''
            }
        }

        stage('执行测试') {
            steps {
                sh '''
                    pytest test_case/ \
                        --enable-midscene \
                        --alluredir=allure-results \
                        -v
                '''
            }
        }

        stage('生成报告') {
            steps {
                allure includeProperties: false, jdk: '',
                    results: [[path: 'allure-results']]
            }
        }
    }

    post {
        always {
            // 清理：停止 Midscene 服务
            sh '''
                pkill -f "node server.js" || true
            '''
            cleanWs()
        }
    }
}
```

**流水线要点：**

1. **服务生命周期**：确保 Midscene 服务在测试前启动，测试后停止
2. **健康检查**：启动后等待服务真正就绪再执行测试
3. **资源清理**：无论成功失败，都要清理进程和工作空间

## 最佳实践总结

经过一段时间的实践，我总结了以下经验：

### 适合用 AI 的场景

| 场景         | 推荐方式 | 原因                       |
| ------------ | -------- | -------------------------- |
| 弹窗处理     | AI       | 弹窗样式多变，AI 更灵活    |
| 表单填写     | AI       | 表单字段名可能变化         |
| 数据验证     | AI 查询  | 结果展示方式可能变化       |
| 页面导航     | 传统     | URL 相对稳定，传统方式更快 |
| 页面加载等待 | 传统     | 等待逻辑固定，无需 AI      |

### 不适合用 AI 的场景

1. **性能要求高的场景**：AI 操作有网络延迟，不适合高频操作
2. **精确验证场景**：需要精确匹配文本时，传统断言更可靠
3. **数据驱动测试**：大量重复用例，传统方式更高效

### 代码组织建议

```
midscene/
├── midscene-bridge/      # Node.js AI 服务
│   ├── server.js         # 服务入口
│   └── package.json      # 依赖配置
├── excel2md.py           # 用例转换工具
├── excel2md/             # Markdown 用例库
└── md2txt/               # 可执行用例

common/
├── midscene_service.py   # 服务管理
└── midscene_helper.py    # AI 操作封装

test_case/
├── test_midscene/        # AI 测试用例
└── conftest.py           # pytest 配置（含失败重试）
```

## 常见问题解答

### Q：AI 操作会不会很慢？

A：确实比传统方式慢。一次 AI 操作约 2-5 秒（取决于网络和模型响应速度）。但考虑到节省的维护时间，这个代价是可以接受的。建议只在必要的地方使用 AI。

### Q：AI 能保证测试结果的稳定性吗？

A：不能 100% 保证。但 AI 有一个优势：它能理解"意图"而不是"具体元素"。当页面改版时，AI 往往能自动适应，减少因选择器变化导致的失败。

### Q：如何调试 AI 操作失败？

A：Midscene 提供了详细的日志和截图。可以在 `midscene_run/dump/` 目录下查看每次操作的详细记录，包括 AI 的思考过程和页面截图。

## 结语

Midscene 不是要取代传统的自动化测试，而是提供了一种新的可能性——让 AI 帮我们处理那些繁琐、易变的部分。在实际项目中，混合使用传统方式和 AI 方式，才能达到最佳效果。

自动化测试的本质是"保证质量"和"提升效率"。如果花费大量时间维护选择器，就偏离了这个初衷。Midscene 让我们把精力从"怎么找到元素"转移到"要验证什么功能"上，这才是自动化测试应该有的样子。
