---
title: SQL高频考点速查手册AI
date: 2026-03-14 13:34:22
tags:
  - SQL
  - 面试
  - 数据库
  - 速查手册
categories:
  - 技术实践
description: 覆盖互联网企业高频 SQL 面试考点，包含窗口函数、分组聚合、JOIN、CTE、TopN、性能优化等实战速查内容。
---

> 覆盖字节跳动、阿里、腾讯、美团、滴滴等互联网大厂高频 SQL 考点

---

**目录**

- [窗口函数（重中之重）](#窗口函数重中之重)
- [分组聚合与 HAVING](#分组聚合与-HAVING)
- [JOIN 连接查询](#JOIN-连接查询)
- [子查询与 CTE](#子查询与-CTE)
- [TopN 问题](#TopN-问题)
- [日期时间函数](#日期时间函数)
- [字符串函数](#字符串函数)
- [条件表达式](#条件表达式)
- [去重与计数技巧](#去重与计数技巧)
- [连续问题（间隔/连续登录）](#连续问题间隔连续登录)
- [行列转换（PIVOT）](#行列转换PIVOT)
- [留存率 / 漏斗分析](#留存率--漏斗分析)
- [性能优化要点](#性能优化要点)
- [附录：高频面试题清单](#附录高频面试题清单)
- [快速参考：SQL 模板库](#快速参考SQL-模板库)

---

## 窗口函数（重中之重）

> **面试出现频率：⭐⭐⭐⭐⭐**  
> 窗口函数是互联网 SQL 面试的核心，几乎必考。

### 基本语法

```sql
函数名() OVER (
    PARTITION BY 分组列
    ORDER BY 排序列 ASC/DESC
    ROWS/RANGE BETWEEN ... AND ...
)
```

### 排名函数对比

| 函数 | 并列时跳号 | 并列时不跳号 | 连续编号 |
|------|-----------|-------------|---------|
| `RANK()` | ✅ 跳号 | — | — |
| `DENSE_RANK()` | — | ✅ 不跳号 | — |
| `ROW_NUMBER()` | — | — | ✅ 强制唯一 |

```sql
-- 经典例题：每个部门薪资前3名
SELECT *
FROM (
    SELECT
        name, dept, salary,
        RANK()       OVER (PARTITION BY dept ORDER BY salary DESC) AS rk,
        DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS drk,
        ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn
    FROM employee
) t
WHERE rk <= 3;
```

### 偏移函数

```sql
-- LAG：取上一行值（常用于同比/环比）
LAG(col, offset, default_val)  OVER (PARTITION BY ... ORDER BY ...)

-- LEAD：取下一行值
LEAD(col, offset, default_val) OVER (PARTITION BY ... ORDER BY ...)

-- 例：计算用户每次登录与上次登录的间隔天数
SELECT
    user_id,
    login_date,
    LAG(login_date, 1) OVER (PARTITION BY user_id ORDER BY login_date) AS last_login,
    DATEDIFF(login_date, LAG(login_date, 1) OVER (PARTITION BY user_id ORDER BY login_date)) AS gap_days
FROM login_log;
```

### 聚合窗口函数（滑动计算）

```sql
-- 近3天滑动平均销售额
SELECT
    dt,
    sales,
    AVG(sales) OVER (
        ORDER BY dt
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS avg_3day
FROM daily_sales;

-- 累计求和
SUM(sales) OVER (PARTITION BY user_id ORDER BY dt ROWS UNBOUNDED PRECEDING)

-- 分组内占比
SUM(sales) OVER (PARTITION BY dept) -- 分母
```

### NTILE 分桶

```sql
-- 将用户按消费金额分成4个等级（四分位）
SELECT
    user_id,
    total_amount,
    NTILE(4) OVER (ORDER BY total_amount DESC) AS quartile
FROM user_order;
```

---

## 分组聚合与 HAVING

> **面试出现频率：⭐⭐⭐⭐⭐**

### 常用聚合函数

```sql
COUNT(*)          -- 统计行数（含NULL）
COUNT(col)        -- 统计非NULL行数
COUNT(DISTINCT col) -- 去重计数
SUM / AVG / MAX / MIN
GROUP_CONCAT(col ORDER BY col SEPARATOR ',')  -- MySQL 拼接字符串
```

### WHERE vs HAVING

```sql
-- WHERE 过滤原始数据（聚合前），不能用聚合函数
-- HAVING 过滤聚合后结果，可以用聚合函数

-- 例：找出订单数 >= 3 且平均金额 > 100 的用户
SELECT user_id, COUNT(*) AS order_cnt, AVG(amount) AS avg_amt
FROM orders
WHERE status = 'paid'          -- 先过滤状态
GROUP BY user_id
HAVING COUNT(*) >= 3           -- 再过滤聚合结果
   AND AVG(amount) > 100;
```

### 执行顺序（必背）

```
FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT
```

---

## JOIN 连接查询

> **面试出现频率：⭐⭐⭐⭐⭐**

### JOIN 类型

```sql
INNER JOIN   -- 取交集（两表都有）
LEFT JOIN    -- 左表全部保留，右表无匹配为 NULL
RIGHT JOIN   -- 右表全部保留，左表无匹配为 NULL
FULL JOIN    -- 取并集（MySQL 不支持，用 UNION 模拟）
CROSS JOIN   -- 笛卡尔积
```

### 常见陷阱

```sql
-- 找出没有下过订单的用户（LEFT JOIN + IS NULL）
SELECT u.user_id
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
WHERE o.user_id IS NULL;

-- 等价写法（NOT EXISTS，性能更优）
SELECT user_id FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.user_id
);

-- FULL JOIN 用 UNION 模拟（MySQL）
SELECT a.*, b.*
FROM a LEFT JOIN b ON a.id = b.id
UNION
SELECT a.*, b.*
FROM a RIGHT JOIN b ON a.id = b.id;
```

### 自连接

```sql
-- 找出薪资高于自己部门平均薪资的员工
SELECT e.name, e.salary, e.dept
FROM employee e
JOIN (
    SELECT dept, AVG(salary) AS avg_sal
    FROM employee
    GROUP BY dept
) avg_t ON e.dept = avg_t.dept
WHERE e.salary > avg_t.avg_sal;
```

---

## 子查询与 CTE

> **面试出现频率：⭐⭐⭐⭐**

### 标量子查询

```sql
-- 查询每个用户的订单数（标量子查询）
SELECT
    user_id,
    (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.user_id) AS order_cnt
FROM users u;
```

### CTE（WITH 语句）—— 推荐写法

```sql
-- 多步骤计算，可读性强，面试加分项
WITH
active_users AS (
    SELECT DISTINCT user_id
    FROM login_log
    WHERE login_date >= '2024-01-01'
),
user_orders AS (
    SELECT user_id, COUNT(*) AS cnt, SUM(amount) AS total
    FROM orders
    WHERE user_id IN (SELECT user_id FROM active_users)
    GROUP BY user_id
)
SELECT au.user_id, COALESCE(uo.cnt, 0) AS order_cnt
FROM active_users au
LEFT JOIN user_orders uo ON au.user_id = uo.user_id;
```

### EXISTS vs IN

```sql
-- IN 适合子查询结果集小的情况
-- EXISTS 适合外表小、子查询表大的情况（短路求值）

-- EXISTS 效率通常更高
SELECT * FROM orders o
WHERE EXISTS (
    SELECT 1 FROM users u
    WHERE u.user_id = o.user_id AND u.vip_level >= 2
);
```

---

## TopN 问题

> **面试出现频率：⭐⭐⭐⭐⭐**

### 全局 TopN

```sql
-- 销售额前5的商品
SELECT product_id, SUM(amount) AS total
FROM orders
GROUP BY product_id
ORDER BY total DESC
LIMIT 5;
```

### 分组 TopN（重点！）

```sql
-- 方法1：窗口函数（推荐，通用）
SELECT *
FROM (
    SELECT
        dept, name, salary,
        DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS dr
    FROM employee
) t
WHERE dr <= 3;

-- 方法2：相关子查询（了解即可）
SELECT *
FROM employee e1
WHERE (
    SELECT COUNT(DISTINCT salary)
    FROM employee e2
    WHERE e2.dept = e1.dept AND e2.salary > e1.salary
) < 3;
```

### 第N高的值

```sql
-- 第二高的薪资
SELECT MAX(salary) AS SecondHighestSalary
FROM employee
WHERE salary < (SELECT MAX(salary) FROM employee);

-- 通用：第N高（用 DENSE_RANK）
SELECT salary
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS dr
    FROM employee
) t
WHERE dr = 2
LIMIT 1;
```

---

## 日期时间函数

> **面试出现频率：⭐⭐⭐⭐**

### 常用函数（MySQL）

```sql
NOW()                          -- 当前日期时间
CURDATE()                      -- 当前日期
DATE(datetime_col)             -- 提取日期部分

-- 格式化
DATE_FORMAT(dt, '%Y-%m-%d')    -- 格式化输出
DATE_FORMAT(dt, '%Y-%m')       -- 年月

-- 计算差值
DATEDIFF(date1, date2)         -- 天数差（date1 - date2）
TIMESTAMPDIFF(HOUR, t1, t2)   -- 小时差
TIMESTAMPDIFF(MONTH, t1, t2)  -- 月份差

-- 加减
DATE_ADD(dt, INTERVAL 7 DAY)   -- 加7天
DATE_SUB(dt, INTERVAL 1 MONTH) -- 减1个月

-- 提取
YEAR(dt) / MONTH(dt) / DAY(dt)
WEEKDAY(dt)   -- 0=周一 ... 6=周日
QUARTER(dt)   -- 季度 1-4
```

### 高频例题

```sql
-- 最近30天的日活统计
SELECT DATE(login_time) AS dt, COUNT(DISTINCT user_id) AS dau
FROM login_log
WHERE login_time >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY DATE(login_time)
ORDER BY dt;

-- 按周/月统计
SELECT DATE_FORMAT(order_time, '%Y-%u') AS week, SUM(amount) AS total
FROM orders
GROUP BY week;
```

---

## 字符串函数

> **面试出现频率：⭐⭐⭐**

```sql
LENGTH(str)                    -- 字节长度
CHAR_LENGTH(str)               -- 字符长度（中文用这个）
CONCAT(s1, s2, ...)            -- 拼接
CONCAT_WS(',', s1, s2)         -- 用分隔符拼接

SUBSTRING(str, pos, len)       -- 截取子串（pos从1开始）
LEFT(str, n)                   -- 取左n个字符
RIGHT(str, n)                  -- 取右n个字符

TRIM(str)                      -- 去除首尾空格
LTRIM / RTRIM                  -- 去左/右空格
REPLACE(str, 'old', 'new')     -- 替换

UPPER(str) / LOWER(str)        -- 大小写转换
LIKE '%关键词%'                 -- 模糊匹配
REGEXP '正则表达式'             -- 正则匹配

-- 例：提取邮箱的域名
SELECT SUBSTRING(email, LOCATE('@', email) + 1) AS domain
FROM users;
```

---

## 条件表达式

> **面试出现频率：⭐⭐⭐⭐**

### CASE WHEN

```sql
-- 简单形式
CASE status
    WHEN 1 THEN '待支付'
    WHEN 2 THEN '已支付'
    ELSE '未知'
END

-- 搜索形式（更灵活）
CASE
    WHEN score >= 90 THEN 'A'
    WHEN score >= 80 THEN 'B'
    WHEN score >= 60 THEN 'C'
    ELSE 'D'
END AS grade

-- 配合聚合使用（行列转换核心）
SUM(CASE WHEN gender = 'M' THEN 1 ELSE 0 END) AS male_cnt
```

### IF / IFNULL / COALESCE / NULLIF

```sql
IF(condition, true_val, false_val)    -- 简单条件
IFNULL(col, 0)                        -- NULL 替换为0
COALESCE(col1, col2, 0)               -- 返回第一个非NULL值
NULLIF(col, 0)                        -- 若col=0则返回NULL（防除零）

-- 防止除零错误
AVG(amount) / NULLIF(COUNT(*), 0)

-- 计算百分比
ROUND(SUM(CASE WHEN status='paid' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS pay_rate
```

---

## 去重与计数技巧

> **面试出现频率：⭐⭐⭐⭐**

```sql
-- UV（独立访客）：去重用户数
COUNT(DISTINCT user_id) AS uv

-- PV（页面浏览量）：不去重
COUNT(*) AS pv

-- 去重后的行（DISTINCT 只能放最前面，对所有列生效）
SELECT DISTINCT user_id, product_id FROM orders;

-- 按条件去重取一条（ROW_NUMBER 推荐）
SELECT *
FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY create_time DESC) AS rn
    FROM orders
) t
WHERE rn = 1;  -- 每个用户只保留最新一条订单
```

---

## 连续问题（间隔/连续登录）

> **面试出现频率：⭐⭐⭐⭐⭐**  
> 这是互联网 SQL 的重难点，字节、美团必考！

### 连续登录 N 天

**核心思路：日期 - ROW_NUMBER = 常数 → 说明连续**

```sql
-- 找出连续登录3天及以上的用户
WITH login_dedup AS (
    -- Step1：去重（同一天多次登录只算一次）
    SELECT DISTINCT user_id, DATE(login_time) AS login_date
    FROM login_log
),
login_group AS (
    -- Step2：日期减去行号，连续日期差值相同
    SELECT
        user_id,
        login_date,
        DATE_SUB(login_date, INTERVAL ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) DAY) AS grp
    FROM login_dedup
),
login_streak AS (
    -- Step3：按(user_id, grp)分组，统计连续天数
    SELECT user_id, grp, COUNT(*) AS streak, MIN(login_date) AS start_dt, MAX(login_date) AS end_dt
    FROM login_group
    GROUP BY user_id, grp
)
SELECT DISTINCT user_id
FROM login_streak
WHERE streak >= 3;
```

### 最长连续登录天数

```sql
-- 在上面基础上，找每个用户的最大连续天数
SELECT user_id, MAX(streak) AS max_streak
FROM login_streak
GROUP BY user_id;
```

### 连续N天都购买的用户

```sql
-- 思路同上，将 login_log 换成 orders 表即可
WITH order_dedup AS (
    SELECT DISTINCT user_id, DATE(order_time) AS order_date
    FROM orders WHERE status = 'paid'
),
order_group AS (
    SELECT user_id, order_date,
        DATE_SUB(order_date, INTERVAL ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_date) DAY) AS grp
    FROM order_dedup
)
SELECT user_id
FROM order_group
GROUP BY user_id, grp
HAVING COUNT(*) >= 7;  -- 连续7天购买
```

---

## 行列转换（PIVOT）

> **面试出现频率：⭐⭐⭐⭐**

### 行转列

```sql
-- 原始数据：(user_id, subject, score)
-- 目标：每个用户的语文、数学、英语成绩各一列

SELECT
    user_id,
    MAX(CASE WHEN subject = '语文' THEN score END) AS chinese,
    MAX(CASE WHEN subject = '数学' THEN score END) AS math,
    MAX(CASE WHEN subject = '英语' THEN score END) AS english
FROM scores
GROUP BY user_id;
```

### 列转行（UNION ALL）

```sql
-- 原始数据：(user_id, chinese, math, english)
-- 目标：展开为(user_id, subject, score)

SELECT user_id, '语文' AS subject, chinese AS score FROM scores
UNION ALL
SELECT user_id, '数学' AS subject, math   AS score FROM scores
UNION ALL
SELECT user_id, '英语' AS subject, english AS score FROM scores;
```

---

## 留存率 / 漏斗分析

> **面试出现频率：⭐⭐⭐⭐⭐**  
> 互联网业务核心指标，产品/数据岗必考！

### 次日留存率

```sql
-- 定义：注册当天登录，第2天也登录 → 次日留存
WITH reg AS (
    SELECT user_id, DATE(reg_time) AS reg_date FROM users
),
login AS (
    SELECT DISTINCT user_id, DATE(login_time) AS login_date FROM login_log
)
SELECT
    r.reg_date,
    COUNT(DISTINCT r.user_id) AS reg_cnt,
    COUNT(DISTINCT l.user_id) AS retained_cnt,
    ROUND(COUNT(DISTINCT l.user_id) / COUNT(DISTINCT r.user_id) * 100, 2) AS retention_rate
FROM reg r
LEFT JOIN login l
    ON r.user_id = l.user_id
    AND l.login_date = DATE_ADD(r.reg_date, INTERVAL 1 DAY)
GROUP BY r.reg_date;
```

### N 日留存（通用模板）

```sql
-- 将上面 INTERVAL 1 DAY 改为 INTERVAL N DAY 即可
-- 常见：次日(1)、3日(3)、7日(7)、30日(30)
```

### 漏斗转化分析

```sql
-- 例：浏览→加购→下单→支付 各步骤转化率
SELECT
    COUNT(DISTINCT CASE WHEN step >= 1 THEN user_id END) AS browse_uv,
    COUNT(DISTINCT CASE WHEN step >= 2 THEN user_id END) AS cart_uv,
    COUNT(DISTINCT CASE WHEN step >= 3 THEN user_id END) AS order_uv,
    COUNT(DISTINCT CASE WHEN step >= 4 THEN user_id END) AS pay_uv,
    ROUND(COUNT(DISTINCT CASE WHEN step >= 2 THEN user_id END) /
          COUNT(DISTINCT CASE WHEN step >= 1 THEN user_id END) * 100, 2) AS browse_to_cart
FROM user_funnel;
```

---

## 性能优化要点

> **面试出现频率：⭐⭐⭐⭐**  
> 中高级岗位必问！

### 索引优化

```sql
-- 建联合索引时，注意最左前缀原则
-- 索引 (a, b, c) 可命中：a, (a,b), (a,b,c)，但不能单独命中 b 或 c

-- 以下写法会导致索引失效：
WHERE LEFT(name, 3) = 'abc'       -- 函数操作
WHERE salary + 1 > 10000          -- 列运算
WHERE status != 1                 -- 负向查询（部分场景）
WHERE name LIKE '%abc'            -- 左模糊（左匹配可以用索引）
```

### 查询优化技巧

```sql
-- 1. 小表驱动大表（LEFT JOIN 时，小表放左边）
-- 2. 避免 SELECT *，只查需要的列
-- 3. 分页优化：深分页避免 OFFSET，用游标分页
-- 不推荐：
SELECT * FROM orders LIMIT 1000000, 10;  -- 扫描100万行再丢弃
-- 推荐：
SELECT * FROM orders WHERE id > 1000000 LIMIT 10;  -- 利用主键索引

-- 4. UNION ALL 比 UNION 快（UNION 会去重，消耗额外资源）
-- 5. EXISTS 通常比 IN 快（子查询结果大时）
-- 6. 覆盖索引：查询的列全在索引中，无需回表
```

### EXPLAIN 分析

| 字段 | 关注点 |
|------|--------|
| `type` | ALL（全表扫描，最差）→ index → range → ref → eq_ref → const（最优） |
| `key` | 实际使用的索引，NULL 表示未走索引 |
| `rows` | 预计扫描行数，越小越好 |
| `Extra` | Using filesort（需优化）、Using temporary（需优化）、Using index（好） |

```sql
EXPLAIN SELECT * FROM orders WHERE user_id = 1001;
```

---

## 附录：高频面试题清单

| # | 题目 | 涉及知识点 |
|---|------|----------|
| 1 | 每个部门薪资最高的员工 | 窗口函数 RANK / 子查询 |
| 2 | 连续登录超过N天的用户 | 连续问题 / ROW_NUMBER |
| 3 | 计算用户次日/7日留存率 | LEFT JOIN / 日期函数 |
| 4 | 找出从未下单的用户 | LEFT JOIN IS NULL / NOT EXISTS |
| 5 | 每个类目销售额Top3商品 | DENSE_RANK 分组TopN |
| 6 | 计算累计销售额（累计求和） | SUM + 窗口函数 ROWS UNBOUNDED |
| 7 | 统计每月新增用户数 | 子查询 / 首次出现日期 |
| 8 | 成绩行转列展示 | CASE WHEN + GROUP BY |
| 9 | 找出同一天既买了A又买了B的用户 | 自连接 / 条件聚合 |
| 10 | 计算每个用户相邻两次购买间隔 | LAG 窗口函数 |
| 11 | 删除重复数据只保留id最小的行 | ROW_NUMBER / 自连接 |
| 12 | 查询近7天的每日销售环比增长率 | LAG + 日期函数 |

---

## 快速参考：SQL 模板库

### 分组 TopN 万能模板
```sql
SELECT * FROM (
    SELECT *, DENSE_RANK() OVER (PARTITION BY 分组列 ORDER BY 排序列 DESC) AS dr
    FROM 表名
) t WHERE dr <= N;
```

### 连续问题万能模板
```sql
WITH t AS (
    SELECT DISTINCT user_id, event_date FROM 表名
),
t2 AS (
    SELECT user_id, event_date,
        DATE_SUB(event_date, INTERVAL ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_date) DAY) AS grp
    FROM t
)
SELECT user_id, COUNT(*) AS streak FROM t2 GROUP BY user_id, grp HAVING streak >= N;
```

### 留存率万能模板
```sql
SELECT
    a.first_date,
    COUNT(DISTINCT a.user_id) AS total,
    COUNT(DISTINCT b.user_id) AS retained,
    ROUND(COUNT(DISTINCT b.user_id) / COUNT(DISTINCT a.user_id), 4) AS rate
FROM 首日表 a
LEFT JOIN 行为表 b
    ON a.user_id = b.user_id
    AND b.event_date = DATE_ADD(a.first_date, INTERVAL N DAY)
GROUP BY a.first_date;
```

---

*最后更新：2026-03*  
*持续更新中，欢迎补充*
