---
title: Python刷题语法速查手册AI
date: 2026-03-13 09:51:43
tags:
  - python
  - 算法
categories:
  - 测开
description: 速查手册
---

# Python 刷题语法速查手册
> 互联网企业技术面试 · LeetCode 知识点全覆盖

---

## 目录

1. [基础数据类型](#1-基础数据类型)
2. [列表 List](#2-列表-List)
3. [字符串 String](#3-字符串-String)
4. [字典 Dict](#4-字典-Dict)
5. [集合 Set](#5-集合-Set)
6. [元组 Tuple](#6-元组-Tuple)
7. [双端队列 deque](#7-双端队列-deque)
8. [堆 heapq](#8-堆-heapq)
9. [排序](#9-排序)
10. [二分查找 bisect](#10-二分查找-bisect)
11. [Counter & defaultdict & OrderedDict](#11-Counter-defaultdict-OrderedDict)
12. [递归与回溯](#12-递归与回溯)
13. [动态规划常用写法](#13-动态规划常用写法)
14. [位运算](#14-位运算)
15. [数学运算](#15-数学运算)
16. [迭代器与生成器](#16-迭代器与生成器)
17. [链表节点 / 树节点定义](#17-链表节点-树节点定义)
18. [图的表示与遍历](#18-图的表示与遍历)
19. [常用内置函数](#19-常用内置函数)
20. [复杂度速记表](#20-复杂度速记表)
21. [ACM 输入输出（笔试模式）](#acm-io)

---

## 1. 基础数据类型

```python
# 整数无限精度，无需担心溢出
a = 10 ** 18

# 浮点数比较
import math
math.isclose(0.1 + 0.2, 0.3)   # True，避免直接 ==

# 整除与取模
7 // 2   # 3
-7 // 2  # -4  (向下取整，注意负数行为)
7 % 2    # 1
-7 % 2   # 1   (结果与除数同号)

# 类型转换
int("42")       # 42
int("ff", 16)   # 255，十六进制转十进制
bin(10)         # '0b1010'
oct(8)          # '0o10'
hex(255)        # '0xff'
ord('A')        # 65
chr(65)         # 'A'

# 无穷大
float('inf')
float('-inf')
```

---

## 2. 列表 List

```python
# 初始化
nums = [0] * n                        # 长度 n，全 0
matrix = [[0] * cols for _ in range(rows)]  # 二维数组（推荐写法）
# 注意：matrix = [[0]*cols]*rows 是浅拷贝，行共享引用，有 BUG

# 增删改查
nums.append(x)          # 末尾追加，O(1)
nums.insert(i, x)       # 指定位置插入，O(n)
nums.pop()              # 弹出末尾，O(1)
nums.pop(i)             # 弹出指定位置，O(n)
nums.remove(x)          # 删除第一个值为 x 的元素，O(n)
del nums[i]             # 删除索引 i 的元素
nums[i] = x             # 修改
nums.index(x)           # 查找 x 的索引，不存在则抛异常
x in nums               # 是否存在，O(n)

# 切片（不修改原列表，返回新列表）
nums[1:4]       # 索引 1~3
nums[::-1]      # 反转
nums[::2]       # 每隔一个取一个

# 列表推导式
squares = [x**2 for x in range(10)]
evens   = [x for x in nums if x % 2 == 0]
flat    = [x for row in matrix for x in row]  # 二维展平

# 常用方法
nums.sort()                  # 原地升序，O(n log n)
nums.sort(reverse=True)      # 原地降序
nums.reverse()               # 原地翻转
sorted(nums)                 # 返回新列表，不改变原列表
len(nums)                    # 长度
sum(nums)                    # 求和
min(nums), max(nums)         # 最小/最大值
nums.count(x)                # 统计 x 出现次数

# 列表拼接
a + b           # 返回新列表
a.extend(b)     # 原地扩展
a += b          # 等同 extend

# 栈（用列表模拟）
stack = []
stack.append(x)   # push
stack.pop()       # pop，取栈顶
stack[-1]         # peek
```

---

## 3. 字符串 String

```python
s = "Hello, World!"

# 基础操作（字符串不可变）
len(s)              # 长度
s[0]                # 'H'
s[-1]               # '!'
s[1:5]              # 'ello'
s[::-1]             # 反转
s + " Python"       # 拼接，效率低，批量拼接用 join

# 常用方法
s.lower()                   # 转小写
s.upper()                   # 转大写
s.strip()                   # 去除两端空白
s.lstrip(), s.rstrip()      # 去除左/右空白
s.replace("Hello", "Hi")    # 替换
s.split(",")                # 按逗号分割，返回列表
s.split()                   # 按空白分割（默认）
",".join(["a","b","c"])     # 'a,b,c'，高效拼接
s.find("llo")               # 返回首次出现索引，不存在返回 -1
s.index("llo")              # 同上，但不存在则抛异常
s.startswith("He")          # True
s.endswith("!")             # True
s.count("l")                # 统计出现次数
s.isdigit()                 # 是否全为数字
s.isalpha()                 # 是否全为字母
s.isalnum()                 # 是否全为字母或数字
s.islower(), s.isupper()    # 是否全小/大写

# 格式化（推荐 f-string）
name, score = "Alice", 99
f"Name: {name}, Score: {score}"

# 字符串与列表互转
list("abc")         # ['a', 'b', 'c']
"".join(['a','b'])  # 'ab'

# ASCII 互转
ord('a')   # 97
chr(97)    # 'a'
ord('A')   # 65

# 字母偏移（常用于字母映射）
offset = ord(c) - ord('a')   # 'a'->0, 'b'->1, ...
```

---

## 4. 字典 Dict

```python
# 初始化
d = {}
d = dict()
d = {"a": 1, "b": 2}

# 增删改查
d["key"] = value          # 添加/更新
d.get("key", default)     # 安全获取，不存在返回 default（默认 None）
d.pop("key")              # 删除并返回，不存在则抛异常
d.pop("key", None)        # 删除并返回，不存在返回 None
del d["key"]              # 删除
"key" in d                # 是否存在 key，O(1)

# 遍历
for k in d:               # 遍历 key
for k, v in d.items():    # 遍历键值对
for v in d.values():      # 遍历 value
for k in d.keys():        # 遍历 key（同第一种）

# 合并
d1.update(d2)             # 将 d2 合并入 d1
d3 = {**d1, **d2}         # 合并为新字典（Python 3.5+）

# 字典推导式
squares = {x: x**2 for x in range(5)}

# setdefault（不存在则初始化）
d.setdefault("key", []).append(val)
```

---

## 5. 集合 Set

```python
# 初始化（注意：{} 是空字典，空集合用 set()）
s = set()
s = {1, 2, 3}
s = set([1, 2, 2, 3])   # {1, 2, 3}，自动去重

# 基础操作，均 O(1) 平均
s.add(x)          # 添加元素
s.remove(x)       # 删除，不存在则抛异常
s.discard(x)      # 删除，不存在不报错
s.pop()           # 随机弹出
x in s            # 是否存在，O(1)
len(s)            # 元素个数

# 集合运算
a | b    # 并集
a & b    # 交集
a - b    # 差集（在 a 不在 b）
a ^ b    # 对称差集（只在其中一个）
a <= b   # a 是否是 b 的子集
a >= b   # a 是否是 b 的超集

# 遍历（无序）
for x in s:
    pass

# 集合推导式
s = {x**2 for x in range(5)}

# frozenset：不可变集合，可作字典 key 或放入另一个集合
fs = frozenset([1, 2, 3])
```

---

## 6. 元组 Tuple

```python
# 元组不可变，可以作字典 key
t = (1, 2, 3)
t = 1, 2, 3        # 等价写法
t = (1,)           # 单元素元组，注意逗号
x, y, z = t        # 解包

# 常用场景
# 1. 作为字典的 key（坐标、状态）
visited = {}
visited[(row, col)] = True

# 2. 多返回值
def func():
    return 1, 2    # 返回元组

a, b = func()

# 3. 命名元组（更清晰）
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
p.x, p.y
```

---

## 7. 双端队列 deque

```python
from collections import deque

# 初始化
q = deque()
q = deque([1, 2, 3])
q = deque(maxlen=k)      # 固定最大长度，超出自动弹出对端

# 操作，两端均 O(1)
q.append(x)              # 右端入队
q.appendleft(x)          # 左端入队
q.pop()                  # 右端出队
q.popleft()              # 左端出队（BFS 常用）
q[0]                     # 查看左端（不删除）
q[-1]                    # 查看右端（不删除）
len(q)                   # 长度
x in q                   # 是否存在，O(n)

# BFS 模板
from collections import deque
def bfs(start):
    queue = deque([start])
    visited = set([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

# 单调队列（滑动窗口最大值）
# deque 存索引，保持队列单调递减
```

---

## 8. 堆 heapq

```python
import heapq

# Python 默认最小堆
heap = []
heapq.heappush(heap, x)      # 入堆，O(log n)
heapq.heappop(heap)          # 弹出最小值，O(log n)
heap[0]                      # 查看堆顶，O(1)
heapq.heapify(nums)          # 列表原地建堆，O(n)

# 最大堆：存负值
heapq.heappush(heap, -x)
val = -heapq.heappop(heap)

# 带优先级的元组
heapq.heappush(heap, (priority, value))

# 求 Top K
heapq.nlargest(k, nums)      # 最大的 k 个，O(n log k)
heapq.nsmallest(k, nums)     # 最小的 k 个，O(n log k)

# 合并多个有序列表
list(heapq.merge([1,3,5], [2,4,6]))   # [1,2,3,4,5,6]
```

---

## 9. 排序

```python
# sorted()：返回新列表，不改变原列表
sorted(nums)                        # 升序
sorted(nums, reverse=True)          # 降序
sorted(nums, key=abs)               # 按绝对值排序
sorted(words, key=len)              # 按字符串长度
sorted(words, key=lambda s: s[::-1])# 按反转后排序

# list.sort()：原地排序，返回 None
nums.sort()
nums.sort(key=lambda x: (x[0], -x[1]))  # 多关键字排序

# 自定义比较（不推荐 cmp，推荐 key）
from functools import cmp_to_key
def compare(a, b):
    # a 在前返回负数，a 在后返回正数
    return int(b+a) - int(a+b)   # 数字拼接最大值经典写法
nums.sort(key=cmp_to_key(compare))

# 常见排序技巧
# 按第二个元素排序
intervals.sort(key=lambda x: x[1])

# 字符串排序（默认字典序）
chars = list("dcba")
chars.sort()   # ['a', 'b', 'c', 'd']
```

---

## 10. 二分查找 bisect

```python
import bisect

# 在有序列表中查找插入位置（保持有序）
bisect.bisect_left(nums, x)    # 返回 x 应插入的最左位置（等于 x 则插在左边）
bisect.bisect_right(nums, x)   # 返回 x 应插入的最右位置（等于 x 则插在右边）
bisect.bisect(nums, x)         # 等同 bisect_right

# 插入（直接修改列表）
bisect.insort_left(nums, x)
bisect.insort_right(nums, x)

# 手写二分模板（面试必备）
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2    # 防止溢出写法（Python 实际无溢出，但保持习惯）
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

# 查找左边界（第一个 >= target 的位置）
def lower_bound(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo   # lo == hi，为插入位置

# 查找右边界（最后一个 <= target 的位置）
def upper_bound(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo - 1
```

---

## 11. Counter & defaultdict & OrderedDict

```python
from collections import Counter, defaultdict, OrderedDict

# ── Counter：计数器 ──────────────────────────────
cnt = Counter("aababc")        # Counter({'a': 3, 'b': 2, 'c': 1})
cnt = Counter([1, 2, 2, 3])
cnt["a"]                       # 3，不存在返回 0（不抛异常）
cnt.most_common(2)             # [('a', 3), ('b', 2)]，最高频 k 个
cnt.total()                    # 总计数（Python 3.10+）
sum(cnt.values())              # 总计数（兼容版本）

# Counter 支持加减法
c1 = Counter("aab")
c2 = Counter("ab")
c1 - c2                        # Counter({'a': 1})，只保留正值
c1 + c2                        # Counter({'a': 3, 'b': 2})
c1 & c2                        # 取最小值
c1 | c2                        # 取最大值

# ── defaultdict：带默认值的字典 ──────────────────
d = defaultdict(int)           # 默认值为 0
d = defaultdict(list)          # 默认值为 []
d = defaultdict(set)           # 默认值为 set()
d = defaultdict(lambda: -1)    # 自定义默认值

d["key"] += 1                  # 不存在也不报错，直接初始化为 0+1=1
d["graph"].append(neighbor)    # 构建邻接表常用写法

# ── OrderedDict：有序字典 ────────────────────────
# Python 3.7+ 普通 dict 已保持插入顺序
# OrderedDict 额外支持 move_to_end
od = OrderedDict()
od["a"] = 1
od.move_to_end("a")            # 移到末尾
od.move_to_end("a", last=False)# 移到开头
od.popitem(last=True)          # 弹出末尾元素（LRU Cache 实现关键）
```

---

## 12. 递归与回溯

```python
import sys
sys.setrecursionlimit(10000)   # 调大递归深度（默认 1000）

# ── 回溯模板 ──────────────────────────────────────
def backtrack(path, choices):
    if 满足结束条件:
        result.append(path[:])   # 注意深拷贝
        return
    for choice in choices:
        if 不满足约束:
            continue
        path.append(choice)      # 做选择
        backtrack(path, 新choices)
        path.pop()               # 撤销选择

# ── 排列问题（元素不重复）──
def permute(nums):
    result = []
    def bt(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]: continue
            used[i] = True
            path.append(nums[i])
            bt(path, used)
            path.pop()
            used[i] = False
    bt([], [False]*len(nums))
    return result

# ── 子集问题 ──
def subsets(nums):
    result = []
    def bt(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            bt(i+1, path)
            path.pop()
    bt(0, [])
    return result
```

---

## 13. 动态规划常用写法

```python
# ── 一维 DP ──────────────────────────────────────
dp = [0] * (n+1)
dp[0] = 初始值
for i in range(1, n+1):
    dp[i] = f(dp[i-1], ...)

# ── 二维 DP ──────────────────────────────────────
dp = [[0]*(n+1) for _ in range(m+1)]
for i in range(1, m+1):
    for j in range(1, n+1):
        dp[i][j] = f(dp[i-1][j], dp[i][j-1], ...)

# ── 记忆化递归（@cache / @lru_cache）────────────
from functools import lru_cache, cache

@cache                          # Python 3.9+，等同无限大 lru_cache
def dp(i, j):
    if 边界条件:
        return 初始值
    return f(dp(i-1, j), dp(i, j-1))

@lru_cache(maxsize=None)        # 兼容写法
def dp(state):
    ...

# 注意：使用 @cache 的函数参数必须可哈希（int, str, tuple，不能是 list）

# ── 背包问题模板 ──────────────────────────────────
# 0-1 背包
dp = [0] * (capacity+1)
for item_weight, item_value in items:
    for j in range(capacity, item_weight-1, -1):   # 逆序！
        dp[j] = max(dp[j], dp[j-item_weight] + item_value)

# 完全背包
dp = [0] * (capacity+1)
for item_weight, item_value in items:
    for j in range(item_weight, capacity+1):        # 正序！
        dp[j] = max(dp[j], dp[j-item_weight] + item_value)
```

---

## 14. 位运算

```python
# 基础运算
a & b    # 按位与
a | b    # 按位或
a ^ b    # 按位异或
~a       # 按位取反（= -a-1）
a << k   # 左移 k 位（= a * 2^k）
a >> k   # 右移 k 位（= a // 2^k）

# 常用技巧
n & 1           # 判断奇偶（1 奇，0 偶）
n & (n-1)       # 消去最低位的 1
n & (-n)        # 保留最低位的 1（lowbit）
n ^ n           # 0，自身异或为 0
n ^ 0           # n，与 0 异或不变
a ^ b ^ a       # b，异或消除

bin(n).count('1')        # 统计 1 的个数
n.bit_length()           # 最高位位置

# 经典应用
# 1. 判断是否是 2 的幂：n > 0 and n & (n-1) == 0
# 2. 只出现一次的数：reduce(xor, nums)
from functools import reduce
from operator import xor
result = reduce(xor, nums)

# 3. 枚举子集（状态压缩）
for mask in range(1 << n):       # 枚举所有 2^n 个子集
    subset = [nums[i] for i in range(n) if mask & (1 << i)]

# 4. 枚举某个 mask 的所有子集
sub = mask
while sub:
    # 处理 sub
    sub = (sub - 1) & mask
```

---

## 15. 数学运算

```python
import math

# 常用函数
math.sqrt(x)         # 开平方
math.ceil(x)         # 向上取整
math.floor(x)        # 向下取整
math.log(x, base)    # 以 base 为底的对数
math.log2(x)         # 以 2 为底
math.log10(x)        # 以 10 为底
math.pow(x, y)       # x^y（返回 float）
pow(x, y, mod)       # x^y % mod（整数，快速幂）
math.gcd(a, b)       # 最大公约数（Python 3.5+）
math.lcm(a, b)       # 最小公倍数（Python 3.9+）
math.factorial(n)    # n 的阶乘
math.comb(n, k)      # 组合数 C(n,k)（Python 3.8+）
math.perm(n, k)      # 排列数 P(n,k)（Python 3.8+）
math.inf             # 正无穷（等同 float('inf')）

# 手写最大公约数（兼容）
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

# 快速幂（Python 内置 pow 已优化）
pow(2, 100, 10**9+7)   # 2^100 mod (10^9+7)

# 常用质数判断
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(math.sqrt(n))+1):
        if n % i == 0:
            return False
    return True

# 取整技巧
(a + b - 1) // b    # 向上整除（ceil(a/b)，不用浮点）
-(-a // b)          # 向上整除（利用 Python 向下取整的特性）
```

---

## 16. 迭代器与生成器

```python
# enumerate：带索引遍历
for i, val in enumerate(nums):
    pass
for i, val in enumerate(nums, start=1):   # 从 1 开始计数
    pass

# zip：并行遍历
for a, b in zip(list1, list2):
    pass
list(zip([1,2,3], ['a','b','c']))   # [(1,'a'), (2,'b'), (3,'c')]

# zip_longest：不等长时用默认值填充
from itertools import zip_longest
for a, b in zip_longest(list1, list2, fillvalue=0):
    pass

# map / filter
list(map(int, ["1","2","3"]))          # [1, 2, 3]
list(filter(lambda x: x>0, nums))     # 过滤正数
list(map(lambda x: x**2, nums))       # 各元素平方

# itertools 常用
from itertools import (
    product,        # 笛卡尔积
    permutations,   # 排列
    combinations,   # 组合
    combinations_with_replacement,  # 可重复组合
    accumulate,     # 前缀和
    chain,          # 连接多个迭代器
    groupby,        # 分组
)

list(permutations([1,2,3], 2))          # 所有 2-排列
list(combinations([1,2,3], 2))          # 所有 2-组合
list(product([0,1], repeat=3))          # 二进制枚举 2^3

# 前缀和（accumulate 默认加法）
from itertools import accumulate
import operator
prefix = list(accumulate(nums))                   # 前缀和
prefix = list(accumulate(nums, initial=0))        # 包含初始值 0
prefix = list(accumulate(nums, operator.mul))     # 前缀积
```

---

## 17. 链表节点 / 树节点定义

```python
# ── 链表节点 ──────────────────────────────────────
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# 虚拟头节点（哨兵）技巧：简化边界处理
dummy = ListNode(0)
dummy.next = head
cur = dummy
# ... 操作 ...
return dummy.next

# ── 二叉树节点 ────────────────────────────────────
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# DFS 遍历（递归）
def preorder(root):
    if not root: return
    visit(root)
    preorder(root.left)
    preorder(root.right)

# BFS 层序遍历
from collections import deque
def levelOrder(root):
    if not root: return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):   # 当前层节点数
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result

# 迭代中序遍历（模拟调用栈）
def inorder(root):
    stack, result = [], []
    cur = root
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        result.append(cur.val)
        cur = cur.right
    return result
```

---

## 18. 图的表示与遍历

```python
from collections import defaultdict, deque

# ── 邻接表 ────────────────────────────────────────
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)   # 无向图

# ── DFS（递归）────────────────────────────────────
def dfs(node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited)

# ── DFS（迭代，用栈）──────────────────────────────
def dfs_iter(start):
    stack = [start]
    visited = {start}
    while stack:
        node = stack.pop()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

# ── BFS（最短路）──────────────────────────────────
def bfs(start, end):
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        node, dist = queue.popleft()
        if node == end:
            return dist
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist+1))
    return -1

# ── 拓扑排序（Kahn 算法）──────────────────────────
def topoSort(n, edges):
    in_degree = [0] * n
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    return order if len(order) == n else []   # 长度不等说明有环

# ── 并查集 ────────────────────────────────────────
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # 路径压缩
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return False
        if self.rank[px] < self.rank[py]:   # 按秩合并
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

---

## 19. 常用内置函数

```python
# 输入输出
input()                    # 读一行（字符串）
int(input())               # 读一个整数
list(map(int, input().split()))  # 读一行整数

# any / all
any(x > 0 for x in nums)  # 任意一个满足
all(x > 0 for x in nums)  # 全部满足

# abs / round
abs(-5)         # 5
round(3.5)      # 4（Python 银行家舍入，3.5->4，2.5->2）
round(3.14159, 2)  # 3.14

# divmod
divmod(7, 3)    # (2, 1)  等同 (7//3, 7%3)

# zip / enumerate（见第 16 节）

# reversed / range
list(reversed([1,2,3]))    # [3,2,1]
range(10, 0, -1)           # 10,9,...,1
range(n-1, -1, -1)         # n-1 倒数到 0

# id / type / isinstance
isinstance(x, (int, float))  # 是否是 int 或 float

# 深浅拷贝
import copy
copy.copy(obj)       # 浅拷贝
copy.deepcopy(obj)   # 深拷贝（嵌套结构用深拷贝）

nums2 = nums[:]      # 列表浅拷贝
nums2 = nums.copy()  # 同上

# print 调试技巧
print(*nums)              # 展开列表打印
print(f"{val=}")          # Python 3.8+，打印变量名和值
```

---

## 20. 复杂度速记表

| 数据结构 / 操作 | 时间复杂度 | 备注 |
|---|---|---|
| 列表 append/pop | O(1) 均摊 | pop(0) 是 O(n) |
| 列表 insert/remove | O(n) | |
| 列表 index (in) | O(n) | |
| 字典 get/set/del | O(1) 均摊 | |
| 集合 add/remove/in | O(1) 均摊 | |
| deque 两端操作 | O(1) | 中间操作 O(n) |
| heapq push/pop | O(log n) | |
| heapq heapify | O(n) | |
| sorted / sort | O(n log n) | Timsort |
| bisect | O(log n) | 要求有序 |
| 字符串拼接 (+=) | O(n²) 累计 | 用 join 代替 |
| "".join(list) | O(n) | |

| 算法 | 时间复杂度 | 空间复杂度 |
|---|---|---|
| 二分查找 | O(log n) | O(1) |
| BFS / DFS | O(V+E) | O(V) |
| 拓扑排序 | O(V+E) | O(V) |
| 并查集（路径压缩+秩）| O(α(n)) ≈ O(1) | O(n) |
| 快速排序 | O(n log n) 均摊 | O(log n) |
| 归并排序 | O(n log n) | O(n) |
| 动态规划（一维） | O(n) | O(n) / O(1) 滚动 |
| 动态规划（二维） | O(mn) | O(mn) / O(n) 滚动 |

---

<span id="acm-io"></span>

## 21. ACM 输入输出（笔试模式）

> 目标：把 LeetCode 风格代码，快速改成 ACM 模式（标准输入/标准输出）。

### 21.1 ACM 模式是什么

- 输入：从标准输入读取（`input()` / `sys.stdin`）
- 输出：打印到标准输出（`print()`）
- 不再有平台给定函数签名，需要自己写 `solve()`

通用结构：

```python
def solve():
    # 读取输入
    # 处理逻辑
    # 输出结果
    pass

if __name__ == "__main__":
    solve()
```

### 21.2 常见输入格式模板

单组输入：

```python
n = int(input().strip())
nums = list(map(int, input().split()))
print(sum(nums))
```

多组输入（第一行给组数 `T`）：

```python
T = int(input().strip())
for _ in range(T):
    a, b = map(int, input().split())
    print(a + b)
```

多组输入（直到 `EOF`）：

```python
while True:
    try:
        a, b = map(int, input().split())
        print(a + b)
    except EOFError:
        break
```

`n` 行矩阵输入：

```python
n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
```

字符串输入：

```python
s = input().strip()
t = input().strip()
print(s == t)
```

### 21.3 大数据量高性能输入

按 token 读取（`sys.stdin.read`）：

```python
import sys

data = sys.stdin.read().strip().split()
idx = 0

n = int(data[idx]); idx += 1
nums = list(map(int, data[idx: idx + n])); idx += n
print(sum(nums))
```

按行读取（`sys.stdin`）：

```python
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    a, b = map(int, line.split())
    print(a + b)
```

### 21.4 输出与改写注意点

- 多个答案逐行 `print(ans)`
- 不要输出多余提示文字（如“结果是：”）
- 题目要求空格分隔时：

```python
arr = [1, 2, 3]
print(" ".join(map(str, arr)))
```

LeetCode -> ACM 改写步骤：

1. 把函数参数改为“从输入读取”
2. 把 `return` 改为 `print`
3. 多组数据时套循环（`T` 组或直到 `EOF`）

### 21.5 一份可直接开写的 ACM 模板

```python
import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    idx = 0
    # 示例：读取 n 和 n 个数
    n = int(data[idx]); idx += 1
    nums = list(map(int, data[idx: idx + n])); idx += n

    ans = sum(nums)
    print(ans)

if __name__ == "__main__":
    solve()
```

### 21.6 常见坑

- `input()` 返回字符串，做数值运算前要 `int()` / `map(int, ...)`
- `split()` 默认按任意空白分割（空格、`\t`）
- 建议对整行输入先 `strip()`，减少首尾空白影响
- `EOF` 题型建议用 `try/except EOFError`
- 不要用 `sum`、`min`、`max` 当变量名，避免覆盖内置函数

---

## 附录：高频面试题对应知识点索引

| 题型 | 核心知识点 |
|---|---|
| 两数之和 / 哈希映射 | `dict.get()`, `in dict` |
| 滑动窗口 | `deque`, 双指针, `Counter` |
| 二叉树 | `TreeNode`, 递归, BFS层序 |
| 链表操作 | `ListNode`, 虚拟头节点, 双指针 |
| 图遍历 / 连通分量 | `defaultdict(list)`, BFS/DFS, 并查集 |
| 前缀和 / 差分 | `accumulate`, `list` |
| 单调栈 | `list` 作栈, `stack[-1]` |
| 堆 / 优先队列 | `heapq`, 最大堆取负 |
| 字符串处理 | `Counter`, `split/join`, `ord/chr` |
| 回溯 / 排列组合 | 递归模板, `path.append/pop` |
| 动态规划 | `@cache`, 滚动数组, 背包 |
| 位运算技巧 | `n&(n-1)`, `xor`, 状压 |
| 数学 / 快速幂 | `pow(a,b,mod)`, `math.gcd` |
| 二分查找 | `bisect`, 手写左右边界模板 |

---

> **版本说明**：本文基于 Python 3.9+，部分语法（如 `@cache`、`math.lcm`、`math.comb`）需 3.8/3.9 以上版本。LeetCode 平台默认支持 Python 3.11+，可放心使用所有特性。
