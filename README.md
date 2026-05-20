<img width="553" height="449" alt="image" src="https://github.com/user-attachments/assets/a7d40790-9c92-48c6-8044-0084e3899d30" /># AI 用户反馈智能分析工作流

## 📋 项目概述

一个面向产品运营人员的 AI 工作流工具，自动分析用户反馈并生成结构化报告。

### 目标用户
- 产品经理 / 产品运营
- 用户增长团队
- 客户服务团队

### 场景与痛点
| 场景 | 传统方式痛点 | AI 解决方案 |
|------|-------------|------------|
| 每日用户反馈处理 | 手动阅读分类，耗时 2-3 小时 | AI 自动分类 + 优先级排序，5 分钟完成 |
| 需求挖掘 | 容易遗漏重要需求 | AI 提取高频需求 + 情感分析 |
| 周报汇报 | 手动整理数据 | 自动生成结构化报告 |

### 下一步验证方式
- A/B 测试：对比 AI 分析 vs 人工分析的准确率
- 用户访谈：收集产品团队使用反馈
- 数据指标：分析效率提升倍数、需求发现数量

---

## 🚀 快速启动

### 环境要求
- Python 3.8+
- API Key（硅基流动 / 其他大模型 API）

### 安装依赖
```bash
pip install requests python-dotenv
```

### 配置 API Key
```bash
# 复制配置文件
copy .env.example .env

# 编辑 .env 文件，填入你的 API Key
```

### 运行方式

#### 方式 0：演示模式（无需 API Key）⭐
```bash
python demo_mode.py
```

#### 方式 1：命令行运行（需要 API Key）
```bash
python main.py
```

#### 方式 2：API 调用（需要 API Key）
```bash
python api_server.py
# 访问 http://localhost:8000/analyze
```

---

## 📤 输入输出示例

### 输入样例
```json
{
  "feedback_list": [
    "APP 打开太慢了，希望能优化一下启动速度",
    "新增的深色模式很好用！但是希望能自定义主题颜色",
    "客服响应太慢，问题三天了还没解决"
  ]
}
```

### 输出样例
```json
{
  "analysis_results": [
    {
      "id": 1,
      "category": "性能问题",
      "priority": "高",
      "sentiment": "负面",
      "keywords": ["启动速度", "优化"],
      "suggested_action": "技术团队排查启动流程"
    }
    // ...
  ],
  "summary": {
    "total": 3,
    "positive": 1,
    "negative": 2,
    "top_issues": ["性能优化", "客服响应"]
  }
}
```

---

## 🤖 AI 协作说明

### 使用的 AI 能力
1. **文本分类** - 自动识别反馈类型（功能建议/BUG/投诉/表扬）
2. **情感分析** - 判断用户情绪（正面/中性/负面）
3. **优先级排序** - 根据影响范围和紧急程度排序
4. **关键词提取** - 提取核心问题点
5. **行动建议** - 生成可执行的处理建议

### AI 工作流
```
用户反馈 → AI 分类 → 情感分析 → 优先级排序 → 生成报告
```

---

## 📁 关键文件说明

| 文件 | 说明 |
|------|------|
| `main.py` | 主程序入口 |
| `ai_workflow.py` | AI 工作流核心逻辑 |
| `api_server.py` | API 服务（可选） |
| `test_samples.json` | 测试样例 |
| `.env.example` | 环境变量模板 |

---

## 🧪 测试样例

运行测试：
```bash
python test_workflow.py
```

---

## 🐛 排错记录

### 问题 1：API 调用超时
**现象**：大量反馈同时处理时超时
**解决**：增加重试机制 + 分批处理

### 问题 2：分类不准确
**现象**：部分反馈分类错误
**解决**：优化 Prompt，增加 few-shot 示例

---


