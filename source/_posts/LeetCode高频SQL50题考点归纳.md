---
title: LeetCode 高频 SQL 50 题考点归纳
date: 2026-03-14 14:01:33
tags:
  - SQL
  - LeetCode
  - 刷题
  - 面试
categories:
  - 技术实践
description: 系统整理 LeetCode「SQL 50 题」七大题型的核心考点、解题套路与高频模板，帮助你快速掌握 SQL 刷题精髓。
---

> LeetCode 官方精选的「SQL 50 题」覆盖了数据库面试的核心知识体系，共分为 7 大类型。本文对每类题目的核心考点、出题规律与解题模板进行系统归纳。

---

**目录**

- [题目分类总览](#题目分类总览)
- [一、Select 基础查询](#一select-基础查询)
- [二、Basic Joins 基础连接](#二basic-joins-基础连接)
- [三、Basic Aggregate Functions 聚合函数](#三basic-aggregate-functions-聚合函数)
- [四、Sorting and Grouping 排序分组](#四sorting-and-grouping-排序分组)
- [五、Advanced Select and Joins 高级查询](#五advanced-select-and-joins-高级查询)
- [六、Subqueries 子查询](#六subqueries-子查询)
- [七、Advanced String Functions 字符串与正则](#七advanced-string-functions-字符串与正则)
- [核心解题模板汇总](#核心解题模板汇总)
- [高频易错点速查](#高频易错点速查)
- [LeetCode SQL 50 题目索引](#leetcode-sql-50-题目索引)

---

## 题目分类总览

| 类别 | 题目数 | 核心考点 | 难度 |
|------|--------|----------|------|
| Select 基础查询 | 5 题 | WHERE / LIKE / NULL 判断 | ⭐ |
| Basic Joins 基础连接 | 9 题 | LEFT JOIN / 自连接 / IS NULL | ⭐⭐ |
| Basic Aggregate Functions 聚合函数 | 8 题 | GROUP BY / HAVING / AVG / ROUND | ⭐⭐ |
| Sorting and Grouping 排序分组 | 10 题 | ORDER BY / 窗口函数 / 连续问题 | ⭐⭐⭐ |
| Advanced Select and Joins 高级查询 | 7 题 | CASE WHEN / UNION / 复杂 JOIN | ⭐⭐⭐ |
| Subqueries 子查询 | 7 题 | 相关子查询 / EXISTS / CTE | ⭐⭐⭐ |
| Advanced String Functions 字符串与正则 | 6 题 | REGEXP / CONCAT / DATE_FORMAT | ⭐⭐ |

---

## 一、Select 基础查询

> **涉及题目**：1757、584、595、1148、1683

### 1. NULL 值判断（高频陷阱）

```sql
-- ❌ 错误：NULL 不能用 = 判断
WHERE referee_id != 2

-- ✅ 正确：NULL 必须用 IS NULL / IS NOT NULL
WHERE referee_id != 2 OR referee_id IS NULL
```

**经典题**：[584. Find Customer Referee](https://leetcode.cn/problems/find-customer-referee/)

```sql
SELECT name
FROM Customer
WHERE referee_id != 2 OR referee_id IS NULL;
```

### 2. 多条件组合过滤

```sql
-- AND / OR 的优先级：AND > OR，复杂条件建议加括号
SELECT name, population, area
FROM World
WHERE area >= 3000000 OR population >= 25000000;
```

**经典题**：[595. Big Countries](https://leetcode.cn/problems/big-countries/)

### 3. 字符串长度判断

```sql
-- CHAR_LENGTH 统计字符数（推荐），LENGTH 统计字节数
SELECT tweet_id
FROM Tweets
WHERE CHAR_LENGTH(content) > 15;
```

**经典题**：[1683. Invalid Tweets](https://leetcode.cn/problems/invalid-tweets/)

### 4. 去重查询

```sql
-- DISTINCT 用于去除重复行（对后面所有列生效）
SELECT DISTINCT author_id AS id
FROM Views
WHERE author_id = viewer_id
ORDER BY id;
```

**经典题**：[1148. Article Views I](https://leetcode.cn/problems/article-views-i/)

**本类速查**

| 考点 | 关键语法 | 常见错误 |
|------|----------|----------|
| NULL 判断 | `IS NULL` / `IS NOT NULL` | 用 `= NULL` |
| 字符串长度 | `CHAR_LENGTH()` | 混用 `LENGTH()` |
| 去重 | `DISTINCT` | 忘记去重导致结果多行 |
| 多条件 | `AND` / `OR` + 括号 | 优先级混乱 |

---

## 二、Basic Joins 基础连接

> **涉及题目**：1378、1068、1581、197、1661、577、1280、570、1934

### 5. LEFT JOIN + IS NULL（找"没有"的数据）

这是本类最高频考点，用于找出一张表中不满足另一张表条件的记录。

```sql
-- 找出访问了但没有下单的用户
SELECT v.customer_id, COUNT(*) AS count_no_trans
FROM Visits v
LEFT JOIN Transactions t ON v.visit_id = t.visit_id
WHERE t.transaction_id IS NULL
GROUP BY v.customer_id;
```

**经典题**：[1581. Customer Who Visited but Did Not Make Any Transactions](https://leetcode.cn/problems/customer-who-visited-but-did-not-make-any-transactions/)

**原理图示**：

```
Visits (左表全保留)    Transactions (右表)
  visit_id             transaction_id
  --------             --------------
     1      ←→ 匹配        有值
     2      ←→ 无匹配    → NULL ← WHERE IS NULL 捕获这行
     3      ←→ 匹配        有值
```

### 6. 自连接（同表比较）

用于同一张表中行与行之间的比较。

```sql
-- 找出比昨天温度更高的日期（自连接）
SELECT w1.id
FROM Weather w1
JOIN Weather w2
    ON DATEDIFF(w1.recordDate, w2.recordDate) = 1
WHERE w1.temperature > w2.temperature;
```

**经典题**：[197. Rising Temperature](https://leetcode.cn/problems/rising-temperature/)

> **注意**：日期比较用 `DATEDIFF()` 而非直接 `-1`，避免跨月/年出错。

### 7. 多表 JOIN 与聚合结合

```sql
-- 统计每台机器的平均处理时间
SELECT
    a1.machine_id,
    ROUND(AVG(a2.timestamp - a1.timestamp), 3) AS processing_time
FROM Activity a1
JOIN Activity a2
    ON a1.machine_id = a2.machine_id
    AND a1.process_id = a2.process_id
    AND a1.activity_type = 'start'
    AND a2.activity_type = 'end'
GROUP BY a1.machine_id;
```

**经典题**：[1661. Average Time of Process per Machine](https://leetcode.cn/problems/average-time-of-process-per-machine/)

### 8. LEFT JOIN 处理"可能不存在"的数据

当右表数据不一定存在时，用 LEFT JOIN + IFNULL/COALESCE 处理。

```sql
-- 查询员工奖金（没有奖金的也要显示）
SELECT e.name, b.bonus
FROM Employee e
LEFT JOIN Bonus b ON e.empId = b.empId
WHERE b.bonus < 1000 OR b.bonus IS NULL;
```

**经典题**：[577. Employee Bonus](https://leetcode.cn/problems/employee-bonus/)

### 9. 三表 JOIN + CROSS JOIN 生成全组合

```sql
-- 统计每个学生每科的考试次数
SELECT
    s.student_id, s.student_name,
    sub.subject_name,
    COUNT(e.subject_name) AS attended_exams
FROM Students s
CROSS JOIN Subjects sub
LEFT JOIN Examinations e
    ON s.student_id = e.student_id
    AND sub.subject_name = e.subject_name
GROUP BY s.student_id, s.student_name, sub.subject_name
ORDER BY s.student_id, sub.subject_name;
```

**经典题**：[1280. Students and Examinations](https://leetcode.cn/problems/students-and-examinations/)

> **技巧**：用 `CROSS JOIN` 生成所有学生×科目的笛卡尔积，再 LEFT JOIN 实际考试记录。

### 10. 管理层查询（统计下属数量）

```sql
-- 找出直属下属数量 >= 5 的经理
SELECT name
FROM Employee
WHERE id IN (
    SELECT managerId
    FROM Employee
    GROUP BY managerId
    HAVING COUNT(*) >= 5
);
```

**经典题**：[570. Managers with at Least 5 Direct Reports](https://leetcode.cn/problems/managers-with-at-least-5-direct-reports/)

**本类速查**

| JOIN 类型 | 含义 | 使用场景 |
|-----------|------|----------|
| `INNER JOIN` | 取两表交集 | 两表都必须有匹配 |
| `LEFT JOIN` | 左表全保留 | 左表数据可能在右表没有对应 |
| `CROSS JOIN` | 笛卡尔积 | 生成所有组合（如题1280） |
| 自连接 | 同表不同别名 | 行与行之间的比较 |

---

## 三、Basic Aggregate Functions 聚合函数

> **涉及题目**：620、1251、1075、1633、1211、1193、1174、550

### 11. AVG + JOIN（加权平均）

```sql
-- 每个产品的平均售价（按销量加权）
SELECT
    p.product_id,
    IFNULL(ROUND(SUM(p.price * u.units) / SUM(u.units), 2), 0) AS average_price
FROM Prices p
LEFT JOIN UnitsSold u
    ON p.product_id = u.product_id
    AND u.purchase_date BETWEEN p.start_date AND p.end_date
GROUP BY p.product_id;
```

**经典题**：[1251. Average Selling Price](https://leetcode.cn/problems/average-selling-price/)

> **注意**：不能直接用 `AVG(price)`，要按 `units` 加权：`SUM(price * units) / SUM(units)`

### 12. ROUND 精度控制

```sql
-- 统计每次查询的质量（quality）和差评率（poor_query_percentage）
SELECT
    query_name,
    ROUND(AVG(rating / position), 2) AS quality,
    ROUND(AVG(IF(rating < 3, 1, 0)) * 100, 2) AS poor_query_percentage
FROM Queries
WHERE query_name IS NOT NULL
GROUP BY query_name;
```

**经典题**：[1211. Queries Quality and Percentage](https://leetcode.cn/problems/queries-quality-and-percentage/)

### 13. 条件聚合（CASE WHEN + SUM/COUNT）

```sql
-- 按月统计各类型交易数量和金额
SELECT
    DATE_FORMAT(trans_date, '%Y-%m') AS month,
    country,
    COUNT(*) AS trans_count,
    SUM(CASE WHEN state = 'approved' THEN 1 ELSE 0 END) AS approved_count,
    SUM(amount) AS trans_total_amount,
    SUM(CASE WHEN state = 'approved' THEN amount ELSE 0 END) AS approved_total_amount
FROM Transactions
GROUP BY DATE_FORMAT(trans_date, '%Y-%m'), country;
```

**经典题**：[1193. Monthly Transactions I](https://leetcode.cn/problems/monthly-transactions-i/)

### 14. 首次行为分析

```sql
-- 即时配送率（首单是否即时配送）
WITH first_order AS (
    SELECT customer_id, MIN(order_date) AS first_date
    FROM Delivery
    GROUP BY customer_id
)
SELECT
    ROUND(
        SUM(CASE WHEN d.order_date = d.customer_pref_delivery_date THEN 1 ELSE 0 END)
        / COUNT(*) * 100, 2
    ) AS immediate_percentage
FROM Delivery d
JOIN first_order f
    ON d.customer_id = f.customer_id
    AND d.order_date = f.first_date;
```

**经典题**：[1174. Immediate Food Delivery II](https://leetcode.cn/problems/immediate-food-delivery-ii/)

### 15. 次日留存率计算

```sql
-- 游戏次日留存率
SELECT
    ROUND(
        COUNT(DISTINCT a2.player_id) / COUNT(DISTINCT a1.player_id),
        2
    ) AS fraction
FROM Activity a1
LEFT JOIN Activity a2
    ON a1.player_id = a2.player_id
    AND a2.event_date = DATE_ADD(a1.event_date, INTERVAL 1 DAY)
WHERE (a1.player_id, a1.event_date) IN (
    SELECT player_id, MIN(event_date) FROM Activity GROUP BY player_id
);
```

**经典题**：[550. Game Play Analysis IV](https://leetcode.cn/problems/game-play-analysis-iv/)

**本类速查**

```sql
COUNT(*)              -- 统计所有行（含 NULL）
COUNT(col)            -- 统计非 NULL 行
COUNT(DISTINCT col)   -- 去重计数
SUM(CASE WHEN ... THEN 1 ELSE 0 END)  -- 条件计数（等价 COUNT IF）
AVG(IF(cond, 1, 0))   -- 条件比率（直接得到小数）
ROUND(value, 2)       -- 保留2位小数
IFNULL(expr, 0)       -- NULL 替换为 0
```

---

## 四、Sorting and Grouping 排序分组

> **涉及题目**：2356、1141、1084、596、185、1789、610、180、1164、1204

### 16. 窗口函数解决分组 TopN（重点）

```sql
-- 每个部门薪资前三（DENSE_RANK 不跳号）
SELECT d.name AS Department, e.name AS Employee, e.salary AS Salary
FROM (
    SELECT
        name, salary, departmentId,
        DENSE_RANK() OVER (PARTITION BY departmentId ORDER BY salary DESC) AS dr
    FROM Employee
) e
JOIN Department d ON e.departmentId = d.id
WHERE e.dr <= 3;
```

**经典题**：[185. Department Top Three Salaries](https://leetcode.cn/problems/department-top-three-salaries/)

### 17. 连续数字问题（LEAD 向前看）

**核心思路**：连续数字 → 相邻行号差固定 → 用 `LEAD` 向前取值比较

```sql
-- 找出连续出现至少3次的数字
WITH cte AS (
    SELECT
        num,
        LEAD(num, 1) OVER (ORDER BY id) AS next1,
        LEAD(num, 2) OVER (ORDER BY id) AS next2
    FROM Logs
)
SELECT DISTINCT num AS ConsecutiveNums
FROM cte
WHERE num = next1 AND num = next2;
```

**经典题**：[180. Consecutive Numbers](https://leetcode.cn/problems/consecutive-numbers/)

### 18. 员工主部门（UNION 条件筛选）

```sql
-- 员工只属于一个部门时返回该部门，属于多个时返回 primary_flag='Y' 的
SELECT employee_id, department_id
FROM Employee
WHERE primary_flag = 'Y'
UNION
SELECT employee_id, department_id
FROM Employee
GROUP BY employee_id
HAVING COUNT(*) = 1;
```

**经典题**：[1789. Primary Department for Each Employee](https://leetcode.cn/problems/primary-department-for-each-employee/)

### 19. 历史价格查询（SCD 缓慢变化维度）

```sql
-- 查询 2019-08-16 时每个产品的价格（变更前的最新价格）
SELECT product_id, new_price AS price
FROM Products
WHERE (product_id, change_date) IN (
    SELECT product_id, MAX(change_date)
    FROM Products
    WHERE change_date <= '2019-08-16'
    GROUP BY product_id
)
UNION
SELECT product_id, 10 AS price
FROM Products
WHERE product_id NOT IN (
    SELECT product_id FROM Products WHERE change_date <= '2019-08-16'
);
```

**经典题**：[1164. Product Price at a Given Date](https://leetcode.cn/problems/product-price-at-a-given-date/)

### 20. 累计求和 + 边界判断

```sql
-- 最后一个能上车不超重的人（累计体重）
WITH cum AS (
    SELECT
        person_id, person_name, weight,
        SUM(weight) OVER (ORDER BY turn) AS cum_weight
    FROM Queue
)
SELECT person_name
FROM cum
WHERE cum_weight <= 1000
ORDER BY cum_weight DESC
LIMIT 1;
```

**经典题**：[1204. Last Person to Fit in the Bus](https://leetcode.cn/problems/last-person-to-fit-in-the-bus/)

### 21. 三角形判断（CASE WHEN 逻辑判断）

```sql
-- 判断三边能否构成三角形
SELECT x, y, z,
    CASE
        WHEN x + y > z AND x + z > y AND y + z > x THEN 'Yes'
        ELSE 'No'
    END AS triangle
FROM Triangle;
```

**经典题**：[610. Triangle Judgement](https://leetcode.cn/problems/triangle-judgement/)

---

## 五、Advanced Select and Joins 高级查询

> **涉及题目**：1907、1978、626、1341、1321、602、585

### 22. UNION ALL 固定分类汇总

```sql
-- 统计低收入、平均收入、高收入各有多少人
SELECT 'Low Salary' AS category, COUNT(*) AS accounts_count
FROM Accounts WHERE income < 20000
UNION ALL
SELECT 'Average Salary', COUNT(*)
FROM Accounts WHERE income BETWEEN 20000 AND 50000
UNION ALL
SELECT 'High Salary', COUNT(*)
FROM Accounts WHERE income > 50000;
```

**经典题**：[1907. Count Salary Categories](https://leetcode.cn/problems/count-salary-categories/)

> **技巧**：`UNION ALL` 比 `UNION` 快（不去重），固定分类用 UNION ALL 拼接更清晰。

### 23. MOD 奇偶行交换（CASE WHEN 精妙用法）

```sql
-- 奇数行与下一行的学生座位互换
SELECT
    CASE
        WHEN id % 2 = 1 AND id = (SELECT COUNT(*) FROM Seat) THEN id
        WHEN id % 2 = 1 THEN id + 1
        ELSE id - 1
    END AS id,
    student
FROM Seat
ORDER BY id;
```

**经典题**：[626. Exchange Seats](https://leetcode.cn/problems/exchange-seats/)

### 24. 多维度排名各取最优（UNION ALL）

```sql
-- 电影评分最高的用户 & 评分最高的电影（各取第一）
(
    SELECT u.name AS results
    FROM MovieRating mr
    JOIN Users u ON mr.user_id = u.user_id
    GROUP BY mr.user_id
    ORDER BY COUNT(*) DESC, u.name ASC
    LIMIT 1
)
UNION ALL
(
    SELECT m.title AS results
    FROM MovieRating mr
    JOIN Movies m ON mr.movie_id = m.movie_id
    WHERE DATE_FORMAT(mr.created_at, '%Y-%m') = '2020-02'
    GROUP BY mr.movie_id
    ORDER BY AVG(mr.rating) DESC, m.title ASC
    LIMIT 1
);
```

**经典题**：[1341. Movie Rating](https://leetcode.cn/problems/movie-rating/)

### 25. 滑动窗口（ROWS BETWEEN）

```sql
-- 餐厅近7天的移动平均消费额
SELECT DISTINCT
    visited_on,
    SUM(amount) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS amount,
    ROUND(AVG(amount) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS average_amount
FROM (
    SELECT visited_on, SUM(amount) AS amount
    FROM Customer
    GROUP BY visited_on
) daily
ORDER BY visited_on
LIMIT 18446744073709551615 OFFSET 6;
```

**经典题**：[1321. Restaurant Growth](https://leetcode.cn/problems/restaurant-growth/)

### 26. 双向关系聚合（UNION ALL 展开）

```sql
-- 拥有最多好友的用户（好友关系是双向的）
SELECT id, COUNT(*) AS num
FROM (
    SELECT requester_id AS id FROM RequestAccepted
    UNION ALL
    SELECT accepter_id AS id FROM RequestAccepted
) t
GROUP BY id
ORDER BY num DESC
LIMIT 1;
```

**经典题**：[602. Friend Requests II: Who Has the Most Friends](https://leetcode.cn/problems/friend-requests-ii-who-has-the-most-friends/)

### 27. 多条件 IN 子查询过滤

```sql
-- 找出 2021 年在不同城市有相同总投保金额的投保人
SELECT id, tiv_2021
FROM Insurance
WHERE tiv_2020 IN (
    SELECT tiv_2020 FROM Insurance GROUP BY tiv_2020 HAVING COUNT(*) > 1
)
AND (lat, lon) IN (
    SELECT lat, lon FROM Insurance GROUP BY lat, lon HAVING COUNT(*) = 1
);
```

**经典题**：[585. Investments in 2016](https://leetcode.cn/problems/investments-in-2016/)

---

## 六、Subqueries 子查询

> **涉及题目**：176、177、178、184、196、1978、262

### 28. 相关子查询（Correlated Subquery）

每行都执行一次子查询，通过外层列与内层列关联。

```sql
-- 找出经理已离职的员工
SELECT employee_id
FROM Employees
WHERE salary < 30000
  AND manager_id NOT IN (
      SELECT employee_id FROM Employees
  )
ORDER BY employee_id;
```

**经典题**：[1978. Employees Whose Manager Left the Company](https://leetcode.cn/problems/employees-whose-manager-left-the-company/)

### 29. 第 N 高的值（DENSE_RANK 通用解法）

```sql
-- 第二高的薪资（不存在则返回 NULL）
SELECT (
    SELECT DISTINCT salary
    FROM Employee
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
) AS SecondHighestSalary;
```

**更通用：支持第 N 高**

```sql
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
    RETURN (
        SELECT salary
        FROM (
            SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS dr
            FROM Employee
        ) t
        WHERE dr = N
        LIMIT 1
    );
END
```

**经典题**：[176. Second Highest Salary](https://leetcode.cn/problems/second-highest-salary/) / [177. Nth Highest Salary](https://leetcode.cn/problems/nth-highest-salary/)

### 30. CTE 分步处理（推荐写法）

CTE（公共表表达式）让复杂查询更易读，面试中是加分项。

```sql
WITH
step1 AS (
    SELECT player_id, MIN(event_date) AS first_login
    FROM Activity
    GROUP BY player_id
),
step2 AS (
    SELECT s.player_id
    FROM step1 s
    JOIN Activity a
        ON s.player_id = a.player_id
        AND a.event_date = DATE_ADD(s.first_login, INTERVAL 1 DAY)
)
SELECT ROUND(COUNT(*) / (SELECT COUNT(DISTINCT player_id) FROM Activity), 2) AS fraction
FROM step2;
```

### 31. EXISTS vs IN 的选择

```sql
-- NOT EXISTS（当子查询结果可能含 NULL 时，比 NOT IN 更安全）
SELECT employee_id
FROM Employees e
WHERE NOT EXISTS (
    SELECT 1 FROM Managers m WHERE m.id = e.manager_id
);

-- NOT IN 的陷阱：若子查询结果含 NULL，整个 NOT IN 结果为空！
-- WHERE manager_id NOT IN (SELECT id FROM Managers)  -- 危险！
```

### 32. 窗口函数嵌套在子查询中使用

窗口函数不能直接出现在 WHERE 中，必须套一层子查询再过滤。

```sql
-- 在子查询中用窗口函数，外层再过滤
SELECT *
FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn
    FROM Employee
) t
WHERE rn = 1;
```

**本类速查**

| 类型 | 写法 | 使用场景 |
|------|------|----------|
| 标量子查询 | `SELECT (SELECT ...)` | 返回单个值 |
| IN 子查询 | `WHERE col IN (SELECT ...)` | 匹配值列表 |
| EXISTS 子查询 | `WHERE EXISTS (SELECT 1 ...)` | 检查是否存在 |
| FROM 子查询 | `FROM (SELECT ...) t` | 派生表 |
| CTE | `WITH t AS (SELECT ...)` | 复杂多步查询（推荐） |

---

## 七、Advanced String Functions 字符串与正则

> **涉及题目**：1667、1527、196、1484、1327、1517

### 33. 大小写规范化（首字母大写）

```sql
-- 修复姓名格式：首字母大写，其余小写
SELECT
    user_id,
    CONCAT(UPPER(LEFT(name, 1)), LOWER(SUBSTRING(name, 2))) AS name
FROM Users
ORDER BY user_id;
```

**经典题**：[1667. Fix Names in a Table](https://leetcode.cn/problems/fix-names-in-a-table/)

### 34. LIKE 模糊匹配 vs REGEXP 正则

```sql
-- LIKE：简单匹配
WHERE conditions LIKE 'DIAB1%'

-- REGEXP：复杂正则（更强大，支持单词边界）
WHERE conditions REGEXP '(^|\\s)DIAB1'
```

**经典题**：[1527. Patients With a Condition](https://leetcode.cn/problems/patients-with-a-condition/)

### 35. 删除重复行（DELETE + 子查询）

```sql
-- 删除重复 Email，只保留 id 最小的行
DELETE FROM Person
WHERE id NOT IN (
    SELECT min_id FROM (
        SELECT MIN(id) AS min_id
        FROM Person
        GROUP BY email
    ) t
);
```

**经典题**：[196. Delete Duplicate Emails](https://leetcode.cn/problems/delete-duplicate-emails/)

> **注意**：MySQL 中不能在 DELETE 的子查询里直接引用同一张表，需要套一层派生表。

### 36. GROUP_CONCAT 聚合字符串

```sql
-- 按日期聚合当天售出的产品（去重，按字母排序，逗号分隔）
SELECT
    sell_date,
    COUNT(DISTINCT product) AS num_sold,
    GROUP_CONCAT(DISTINCT product ORDER BY product SEPARATOR ',') AS products
FROM Activities
GROUP BY sell_date
ORDER BY sell_date;
```

**经典题**：[1484. Group Sold Products By The Date](https://leetcode.cn/problems/group-sold-products-by-the-date/)

### 37. 邮箱格式正则验证

```sql
-- 验证合法的邮箱格式
SELECT user_id, name, mail
FROM Users
WHERE mail REGEXP '^[a-zA-Z][a-zA-Z0-9_.-]*@leetcode\\.com$';
```

**正则说明**：

- `^[a-zA-Z]`：以字母开头
- `[a-zA-Z0-9_.-]*`：中间可含字母、数字、`_`、`.`、`-`
- `@leetcode\\.com$`：以 `@leetcode.com` 结尾（`.` 需转义）

**经典题**：[1517. Find Users With Valid E-Mails](https://leetcode.cn/problems/find-users-with-valid-e-mails/)

### 38. 日期格式化 + 条件过滤

```sql
-- 查询特定月份订购数量 >= 100 的产品
SELECT product_id, product_name
FROM Products
WHERE product_id IN (
    SELECT product_id
    FROM Orders
    WHERE DATE_FORMAT(order_date, '%Y-%m') = '2020-02'
    GROUP BY product_id
    HAVING SUM(unit) >= 100
);
```

**经典题**：[1327. List the Products Ordered in a Period](https://leetcode.cn/problems/list-the-products-ordered-in-a-period/)

**本类速查**

```sql
-- 大小写
UPPER(str) / LOWER(str)
CONCAT(UPPER(LEFT(str,1)), LOWER(SUBSTRING(str,2)))  -- 首字母大写

-- 截取
LEFT(str, n)             -- 左取 n 个字符
RIGHT(str, n)            -- 右取 n 个字符
SUBSTRING(str, pos, len) -- 从 pos 位置取 len 个（pos 从 1 开始）

-- 查找
LOCATE(substr, str)      -- 返回子串位置（找不到返回 0）

-- 替换与拼接
REPLACE(str, 'old', 'new')
CONCAT_WS(',', s1, s2)   -- 用分隔符连接（忽略 NULL）
GROUP_CONCAT(col ORDER BY col SEPARATOR ',')  -- 聚合拼接

-- 正则
REGEXP '正则表达式'
REGEXP_REPLACE(str, pattern, replacement)    -- MySQL 8.0+
```

---

## 核心解题模板汇总

### 模板1：分组 TopN

```sql
SELECT *
FROM (
    SELECT
        *,
        DENSE_RANK() OVER (PARTITION BY 分组列 ORDER BY 排序列 DESC) AS dr
    FROM 表名
) t
WHERE dr <= N;
```

### 模板2：LEFT JOIN + IS NULL（找"没有"的数据）

```sql
SELECT a.id
FROM 主表 a
LEFT JOIN 关联表 b ON a.id = b.aid AND [其他条件]
WHERE b.id IS NULL;
```

### 模板3：连续问题（日期 - 行号 = 常数）

```sql
WITH dedup AS (
    SELECT DISTINCT user_id, event_date FROM 表名
),
grouped AS (
    SELECT
        user_id, event_date,
        DATE_SUB(event_date,
            INTERVAL ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_date) DAY
        ) AS grp
    FROM dedup
)
SELECT user_id, COUNT(*) AS streak
FROM grouped
GROUP BY user_id, grp
HAVING streak >= N;
```

### 模板4：留存率

```sql
SELECT
    ROUND(COUNT(DISTINCT b.user_id) / COUNT(DISTINCT a.user_id), 2) AS rate
FROM 首次行为表 a
LEFT JOIN 行为表 b
    ON a.user_id = b.user_id
    AND b.event_date = DATE_ADD(a.first_date, INTERVAL N DAY);
```

### 模板5：条件聚合（行列转换核心）

```sql
SELECT
    group_col,
    SUM(CASE WHEN type = 'A' THEN value ELSE 0 END) AS type_a,
    SUM(CASE WHEN type = 'B' THEN value ELSE 0 END) AS type_b,
    COUNT(CASE WHEN type = 'C' THEN 1 END) AS type_c_cnt
FROM 表名
GROUP BY group_col;
```

### 模板6：滑动窗口聚合

```sql
SELECT
    dt,
    SUM(value) OVER (ORDER BY dt ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS sum_7day,
    AVG(value) OVER (ORDER BY dt ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS avg_7day
FROM 日汇总表;
```

---

## 高频易错点速查

| 易错点 | 错误写法 | 正确写法 |
|--------|----------|----------|
| NULL 比较 | `col = NULL` | `col IS NULL` |
| NOT IN 含 NULL | `NOT IN (子查询含NULL)` | 改用 `NOT EXISTS` |
| 删除重复行 | `DELETE ... WHERE id NOT IN (SELECT MIN(id) FROM t ...)` | 多套一层子查询绕过 MySQL 限制 |
| 字符长度（中文） | `LENGTH(name)` | `CHAR_LENGTH(name)` |
| 日期差（跨月） | `date1 - date2` | `DATEDIFF(date1, date2)` |
| 精确保留小数 | 直接返回浮点 | `ROUND(val, 2)` |
| UNION 去重慢 | `UNION` | 不需要去重时用 `UNION ALL` |
| 窗口函数 WHERE | `WHERE RANK() <= 3` | 外层套子查询再 `WHERE dr <= 3` |
| 深分页 | `LIMIT 100000, 10` | `WHERE id > 100000 LIMIT 10` |

---

## LeetCode SQL 50 题目索引

| # | 题号 | 题目 | 类别 | 核心考点 |
|---|------|------|------|----------|
| 1 | 1757 | Recyclable and Low Fat Products | Select | WHERE 多条件 |
| 2 | 584 | Find Customer Referee | Select | IS NULL 判断 |
| 3 | 595 | Big Countries | Select | OR 条件 |
| 4 | 1148 | Article Views I | Select | DISTINCT |
| 5 | 1683 | Invalid Tweets | Select | CHAR_LENGTH |
| 6 | 1378 | Replace Employee ID With The Unique Identifier | Basic Joins | LEFT JOIN |
| 7 | 1068 | Product Sales Analysis I | Basic Joins | INNER JOIN |
| 8 | 1581 | Customer Who Visited but Did Not Make Any Transactions | Basic Joins | LEFT JOIN + IS NULL |
| 9 | 197 | Rising Temperature | Basic Joins | 自连接 + DATEDIFF |
| 10 | 1661 | Average Time of Process per Machine | Basic Joins | 自连接 + AVG |
| 11 | 577 | Employee Bonus | Basic Joins | LEFT JOIN + IS NULL |
| 12 | 1280 | Students and Examinations | Basic Joins | CROSS JOIN + LEFT JOIN |
| 13 | 570 | Managers with at Least 5 Direct Reports | Basic Joins | 子查询 + HAVING |
| 14 | 1934 | Confirmation Rate | Basic Joins | 条件 AVG |
| 15 | 620 | Not Boring Movies | Aggregate | WHERE + ORDER BY |
| 16 | 1251 | Average Selling Price | Aggregate | 加权 AVG + BETWEEN |
| 17 | 1075 | Project Employees I | Aggregate | LEFT JOIN + AVG ROUND |
| 18 | 1633 | Percentage of Users Attended a Contest | Aggregate | 子查询 + 百分比 |
| 19 | 1211 | Queries Quality and Percentage | Aggregate | 条件 AVG |
| 20 | 1193 | Monthly Transactions I | Aggregate | DATE_FORMAT + 条件聚合 |
| 21 | 1174 | Immediate Food Delivery II | Aggregate | 首次行为 + 条件计数 |
| 22 | 550 | Game Play Analysis IV | Aggregate | 次日留存率 |
| 23 | 2356 | Number of Unique Subjects Taught by Each Teacher | Sorting | COUNT DISTINCT |
| 24 | 1141 | User Activity for the Past 30 Days I | Sorting | 日期范围 + COUNT DISTINCT |
| 25 | 1084 | Sales Analysis III | Sorting | HAVING + 日期范围 |
| 26 | 596 | Classes More Than 5 Students | Sorting | GROUP BY + HAVING COUNT |
| 27 | 185 | Department Top Three Salaries | Sorting | DENSE_RANK 分组TopN |
| 28 | 1789 | Primary Department for Each Employee | Sorting | UNION + HAVING |
| 29 | 610 | Triangle Judgement | Sorting | CASE WHEN 三角不等式 |
| 30 | 180 | Consecutive Numbers | Sorting | LEAD 连续判断 |
| 31 | 1164 | Product Price at a Given Date | Sorting | 历史价格 UNION |
| 32 | 1204 | Last Person to Fit in the Bus | Sorting | 累计求和窗口函数 |
| 33 | 1907 | Count Salary Categories | Adv Select | UNION ALL 分类汇总 |
| 34 | 1978 | Employees Whose Manager Left the Company | Adv Select | NOT IN 子查询 |
| 35 | 626 | Exchange Seats | Adv Select | CASE WHEN + MOD |
| 36 | 1341 | Movie Rating | Adv Select | UNION ALL + 分别排序 |
| 37 | 1321 | Restaurant Growth | Adv Select | 滑动窗口 ROWS BETWEEN |
| 38 | 602 | Friend Requests II: Who Has the Most Friends | Adv Select | UNION ALL 双向关系 |
| 39 | 585 | Investments in 2016 | Adv Select | 多条件 IN 子查询 |
| 40 | 176 | Second Highest Salary | Subqueries | LIMIT OFFSET / DENSE_RANK |
| 41 | 177 | Nth Highest Salary | Subqueries | 自定义函数 + DENSE_RANK |
| 42 | 178 | Rank Scores | Subqueries | DENSE_RANK 全局排名 |
| 43 | 184 | Department Highest Salary | Subqueries | 子查询 + JOIN |
| 44 | 196 | Delete Duplicate Emails | Subqueries | DELETE + 子查询 |
| 45 | 1978 | Employees Whose Manager Left the Company | Subqueries | NOT IN 相关子查询 |
| 46 | 262 | Trips and Users | Subqueries | 多条件过滤 + 条件聚合 |
| 47 | 1667 | Fix Names in a Table | String Func | UPPER + LEFT + SUBSTRING |
| 48 | 1527 | Patients With a Condition | String Func | LIKE / REGEXP |
| 49 | 1484 | Group Sold Products By The Date | String Func | GROUP_CONCAT |
| 50 | 1517 | Find Users With Valid E-Mails | String Func | REGEXP 邮箱验证 |

---

*整理于 2026-03，持续更新*
