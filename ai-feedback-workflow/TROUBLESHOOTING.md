# 排错记录

## 问题 1：依赖安装后导入失败

**时间**：2026-05-20 20:15

**现象**：
```
ModuleNotFoundError: No module named 'requests'
```

**排查过程**：
1. 检查是否安装：`pip list | findstr requests` ✓ 已安装
2. 检查 Python 环境：发现有多个 Python 版本
3. 确认 pip 和 python 是否同一环境

**解决方案**：
```bash
# 使用 python -m pip 确保安装到正确的环境
python -m pip install requests python-dotenv
```

**AI 协助**：
- 询问 "ModuleNotFoundError 但已安装怎么办"
- AI 建议检查 Python 环境一致性

---

## 问题 2：API Key 配置问题

**时间**：2026-05-20 20:18

**现象**：
```
401 Unauthorized - Invalid API Key
```

**排查过程**：
1. 检查 .env 文件是否存在 ✓
2. 检查 API Key 格式 ✓
3. 检查是否正确加载环境变量

**解决方案**：
```python
from dotenv import load_dotenv
load_dotenv()  # 确保在导入 API_KEY 之前调用
```

**AI 协助**：
- AI 指出 load_dotenv() 调用位置问题
- 建议在导入环境变量前先加载

---

## 问题 3：JSON 解析失败

**时间**：2026-05-20 20:22

**现象**：
```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**排查过程**：
1. 打印 API 返回的原始内容
2. 发现内容包含 markdown 代码块标记：
   ```json
   {
     "category": "..."
   }
   ```

**解决方案**：
```python
content = content.strip()
if content.startswith("```json"):
    content = content[7:-3]  # 移除 ```json 和 ```
elif content.startswith("```"):
    content = content[3:-3]  # 移除 ``` 和 ```
analysis = json.loads(content)
```

**AI 协助**：
- AI 识别出是大模型返回 markdown 格式
- 提供字符串处理代码

---

## 问题 4：API 超时

**时间**：2026-05-20 20:25

**现象**：
```
requests.exceptions.Timeout: HTTPConnectionPool timeout
```

**排查过程**：
1. 检查网络连接 ✓
2. 测试 API 端点可达性 ✓
3. 默认 timeout 太短（10 秒）

**解决方案**：
```python
response = requests.post(
    API_URL,
    headers=self.headers,
    json=payload,
    timeout=30  # 增加到 30 秒
)
```

**AI 协助**：
- AI 建议增加 timeout 参数
- 建议添加重试机制（后续优化）

---

## 问题 5：分类结果不一致

**时间**：2026-05-20 20:30

**现象**：
- 同样的反馈，多次运行结果不同
- 有时分类为"功能建议"，有时为"BUG 投诉"

**排查过程**：
1. 检查 temperature 参数：默认 0.7，随机性较高
2. 检查 Prompt 是否清晰

**解决方案**：
```python
# 降低 temperature，提高确定性
"temperature": 0.3,  # 从 0.7 改为 0.3

# 在 Prompt 中增加明确的判断标准
判断标准：
- 优先级高：影响核心功能、严重 BUG、VIP 用户问题
- 优先级中：功能优化、一般问题
- 优先级低：体验优化、个性化需求
```

**AI 协助**：
- AI 解释 temperature 参数作用
- 帮助优化 Prompt 增加判断标准

---

## 总结

| 问题 | 类型 | 解决时间 | AI 贡献 |
|------|------|---------|--------|
| 依赖导入 | 环境配置 | 5 分钟 | 环境检查建议 |
| API Key | 配置问题 | 3 分钟 | 定位 load_dotenv 位置 |
| JSON 解析 | 数据格式 | 10 分钟 | 提供字符串处理代码 |
| API 超时 | 网络问题 | 5 分钟 | timeout 参数建议 |
| 分类不一致 | 模型参数 | 15 分钟 | temperature 解释 + Prompt 优化 |

**关键学习**：
1. 环境配置要仔细，特别是多 Python 版本
2. 大模型输出格式不稳定，需要后处理
3. temperature 参数影响输出一致性
4. Prompt 越清晰，结果越可靠
