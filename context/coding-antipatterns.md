# Coding Anti-Patterns

来源：Karpathy LLM 编码误区观察 + workspace 经验整理。
配合 `.claude/rules/10-coding.md` 使用。每条都含反例和修法。

---

## 1. Think Before Coding（假设之前先澄清）

### 反例 1：隐藏假设

**用户请求**：`添加导出用户数据的功能`

❌ LLM 通常做法：

```python
def export_users(format='json'):
    users = User.query.all()
    if format == 'json':
        with open('users.json', 'w') as f:
            json.dump([u.to_dict() for u in users], f)
    elif format == 'csv':
        with open('users.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'email', 'name'])
            writer.writeheader()
            writer.writerows([u.to_dict() for u in users])
    return f"Exported {len(users)} users"
```

问题：
- 默默假设导出全部用户（分页？隐私？）
- 默默假设输出位置
- 默默假设字段集合
- 默默假设 CSV 字段名

✅ 正确做法：先列假设，问清楚。

```
开工前需要澄清：
1. 范围：全部用户还是过滤子集？
2. 形式：浏览器下载、后台任务+邮件、还是 API 端点？
3. 字段：哪些字段？（部分可能敏感）
4. 体量：用户数量级？（影响实现）

最简方案：API 端点返回分页 JSON。
文件导出需要更多信息。
```

### 反例 2：多种解释静默选一个

**用户请求**：`让搜索更快`

❌ LLM：直接上 cache + index + async，写 200 行。

✅ 先问：
- 响应时间快？(< 100ms)
- 并发吞吐量大？
- 感知速度快？(渐进渲染)
当前搜索 ~500ms。哪个最关键？

---

## 2. Simplicity First（要什么写什么）

### 反例 1：过度抽象

**用户请求**：`加一个计算折扣的函数`

❌ LLM：

```python
class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float: ...

class PercentageDiscount(DiscountStrategy): ...
class FixedDiscount(DiscountStrategy): ...

@dataclass
class DiscountConfig:
    strategy: DiscountStrategy
    min_purchase: float = 0.0
    max_discount: float = float('inf')

class DiscountCalculator:
    def __init__(self, config): ...
    def apply_discount(self, amount): ...
# 30+ 行 setup 才能算一次折扣
```

✅ 简单版：

```python
def calculate_discount(amount: float, percent: float) -> float:
    return amount * (percent / 100)
```

什么时候加复杂度：实际需要多种折扣类型时再重构，不要现在。

### 反例 2：投机功能

**用户请求**：`把用户偏好存到数据库`

❌ LLM：写 `PreferenceManager` 类带 cache / validator / merge / notify 四个开关，60 行。

✅ 正确：

```python
def save_preferences(db, user_id: int, preferences: dict):
    db.execute(
        "UPDATE users SET preferences = ? WHERE id = ?",
        (json.dumps(preferences), user_id)
    )
```

cache、validation、merge 等等以后真有需求再加。

---

## 3. Surgical Changes（只改必要的行）

### 反例 1：顺手重构

**用户请求**：`修复 email 为空时校验器崩溃的 bug`

❌ LLM diff：

```diff
  def validate_user(user_data):
-     if not user_data.get('email'):
+     """Validate user data."""
+     email = user_data.get('email', '').strip()
+     if not email:
          raise ValueError("Email required")
-     if '@' not in user_data['email']:
+     if '@' not in email or '.' not in email.split('@')[1]:
          raise ValueError("Invalid email")
-     if not user_data.get('username'):
+     username = user_data.get('username', '').strip()
+     if not username:
          raise ValueError("Username required")
+     if len(username) < 3:
+         raise ValueError("Username too short")
+     if not username.isalnum():
+         raise ValueError("Username must be alphanumeric")
      return True
```

问题：
- "顺便"加强了 email 校验
- "顺便"加了 username 长度和字符校验
- 改了注释
- 加了 docstring

✅ 外科手术：

```diff
  def validate_user(user_data):
      # Check email format
-     if not user_data.get('email'):
+     email = user_data.get('email', '')
+     if not email or not email.strip():
          raise ValueError("Email required")
      # Basic email validation
-     if '@' not in user_data['email']:
+     if '@' not in email:
          raise ValueError("Invalid email")
      if not user_data.get('username'):
          raise ValueError("Username required")
      return True
```

只改 email 空值处理那几行。

### 反例 2：风格漂移

**用户请求**：`给 upload 函数加日志`

❌ LLM：顺便把单引号改双引号、加 type hint、加 docstring、改 boolean 返回逻辑。

✅ 匹配现有风格：保留单引号，不加 type hint，只插入 logger 调用。

```diff
+ import logging
+ logger = logging.getLogger(__name__)
+
  def upload_file(file_path, destination):
+     logger.info(f'Starting upload: {file_path}')
      try:
          with open(file_path, 'rb') as f:
              data = f.read()
          response = requests.post(destination, files={'file': data})
          if response.status_code == 200:
+             logger.info(f'Upload successful: {file_path}')
              return True
          else:
+             logger.error(f'Upload failed: {file_path}, status={response.status_code}')
              return False
      except Exception as e:
-         print(f"Error: {e}")
+         logger.exception(f'Upload error: {file_path}')
          return False
```

---

## 4. Goal-Driven Execution（成功标准先于动作）

### 反例 1：模糊 vs 可验证

**用户请求**：`修一下认证系统`

❌ LLM：

```
我会:
1. review 代码
2. 找问题
3. 改进
4. 测试
[然后就乱改]
```

✅ 先要可验证目标：

```
"修认证"需要明确成功标准。具体是哪个问题？

如果是"改密码后用户仍能用旧 session 登录"：

计划：
1. 写测试：改密码 → 验证旧 session 被废 → 测试当前失败（复现 bug）
2. 实现：改密码时废 session → 测试通过
3. 边缘情况：多 session、并发改密码 → 额外测试
4. 不回归：现有 auth 测试仍绿
```

### 反例 2：一次性大改

**用户请求**：`给 API 加 rate limit`

❌ LLM：一个 commit 300 行，Redis + 多策略 + 配置 + 监控全堆上。

✅ 增量+逐步验证：

```
1. 内存版（单 endpoint）→ 验证：curl 11 次第 11 次 429
2. 抽 middleware（全 endpoint）→ 验证：/users 和 /posts 都限流
3. Redis 后端（多机）→ 验证：重启后限额持久；两实例共享计数
4. 配置化（每 endpoint 独立速率）→ 验证：/search 10/min，/users 100/min
```

### 反例 3：不先复现就修

**用户请求**：`排序在分数相同时崩了`

❌ LLM：直接改 sort key，不写测试。

✅ 先复现再修：

```python
# 1. 写复现测试
def test_sort_with_duplicate_scores():
    scores = [
        {'name': 'Alice', 'score': 100},
        {'name': 'Bob', 'score': 100},
        {'name': 'Charlie', 'score': 90},
    ]
    result = sort_scores(scores)
    assert result[0]['score'] == 100
    assert result[1]['score'] == 100

# 验证：跑 10 次 → 失败（顺序不稳定）

# 2. 用稳定排序修
def sort_scores(scores):
    return sorted(scores, key=lambda x: (-x['score'], x['name']))

# 验证：测试稳定通过
```

---

## 反模式总览

| 原则 | 反模式 | 修法 |
|------|--------|------|
| Think Before | 默默选格式、字段、范围 | 先列假设再问 |
| Simplicity | 单一计算用 Strategy 模式 | 一个函数就够 |
| Surgical | 修 bug 顺便改格式/加 type hint | 只改与请求相关的行 |
| Goal-Driven | "我会 review 并改进" | "写测试复现 → 让它过 → 不回归" |

---

## 核心洞察

"过度复杂"的代码不是显然错的——它遵循设计模式和最佳实践。**问题是时机**：在需要之前就引入复杂度，会带来：

- 更难理解
- 引入更多 bug
- 实现时间更长
- 更难测试

简单版本：

- 易懂
- 实现快
- 易测试
- 真正需要时再重构

**好代码 = 简单解决今天的问题，不是提前解决明天的问题。**

---

来源参考：[forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) EXAMPLES.md（MIT），引用 Karpathy LLM coding 观察。
