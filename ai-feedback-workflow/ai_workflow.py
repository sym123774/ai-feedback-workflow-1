"""
AI 用户反馈智能分析工作流
核心工作流模块
"""

import os
import json
import requests
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

# 配置 API（使用硅基流动或其他大模型 API）
API_KEY = os.getenv("API_KEY", "")
API_URL = os.getenv("API_URL", "https://api.siliconflow.cn/v1/chat/completions")
MODEL = os.getenv("MODEL", "Pro/deepseek-ai/DeepSeek-V3")


class FeedbackAnalyzer:
    """用户反馈分析器"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def analyze_single_feedback(self, feedback: str) -> Dict:
        """分析单条反馈"""
        
        prompt = f"""
你是一个专业的产品运营分析师。请分析以下用户反馈：

用户反馈："{feedback}"

请按照以下 JSON 格式返回分析结果（只返回 JSON，不要其他内容）：
{{
    "category": "反馈类型（功能建议/BUG 投诉/使用咨询/表扬感谢/其他）",
    "priority": "优先级（高/中/低）",
    "sentiment": "情感倾向（正面/中性/负面）",
    "keywords": ["关键词 1", "关键词 2"],
    "summary": "一句话总结",
    "suggested_action": "建议处理动作"
}}

判断标准：
- 优先级高：影响核心功能、严重 BUG、VIP 用户问题
- 优先级中：功能优化、一般问题
- 优先级低：体验优化、个性化需求
"""
        
        try:
            response = requests.post(
                API_URL,
                headers=self.headers,
                json={
                    "model": MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 500
                },
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # 解析 JSON 结果
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
            
            analysis = json.loads(content)
            analysis["original_feedback"] = feedback
            return analysis
            
        except Exception as e:
            return {
                "original_feedback": feedback,
                "error": str(e),
                "category": "未知",
                "priority": "中",
                "sentiment": "中性",
                "keywords": [],
                "summary": "分析失败",
                "suggested_action": "人工复核"
            }
    
    def analyze_batch(self, feedback_list: List[str]) -> Dict:
        """批量分析反馈"""
        results = []
        
        for i, feedback in enumerate(feedback_list, 1):
            print(f"分析中 ({i}/{len(feedback_list)}): {feedback[:30]}...")
            analysis = self.analyze_single_feedback(feedback)
            analysis["id"] = i
            results.append(analysis)
        
        # 生成汇总报告
        summary = self._generate_summary(results)
        
        return {
            "analysis_results": results,
            "summary": summary,
            "total_processed": len(results)
        }
    
    def _generate_summary(self, results: List[Dict]) -> Dict:
        """生成汇总报告"""
        categories = {}
        sentiments = {"正面": 0, "中性": 0, "负面": 0}
        priorities = {"高": [], "中": [], "低": []}
        
        for r in results:
            # 分类统计
            cat = r.get("category", "其他")
            categories[cat] = categories.get(cat, 0) + 1
            
            # 情感统计
            sent = r.get("sentiment", "中性")
            if sent in sentiments:
                sentiments[sent] += 1
            
            # 高优先级问题收集
            if r.get("priority") == "高":
                priorities["高"].append(r.get("summary", ""))
        
        return {
            "total": len(results),
            "by_category": categories,
            "by_sentiment": sentiments,
            "high_priority_issues": priorities["高"][:5],  # 最多 5 个
            "positive_rate": round(sentiments["正面"] / len(results) * 100, 1) if results else 0
        }


def main():
    """主函数 - 演示模式"""
    print("=" * 60)
    print("AI 用户反馈智能分析工作流")
    print("=" * 60)
    
    # 测试样例
    test_feedbacks = [
        "APP 打开太慢了，希望能优化一下启动速度",
        "新增的深色模式很好用！但是希望能自定义主题颜色",
        "客服响应太慢，问题三天了还没解决",
        "这个功能完全没法用，一直报错",
        "界面设计很漂亮，用户体验不错",
        "希望能增加导出 Excel 的功能"
    ]
    
    print(f"\n待分析反馈数量：{len(test_feedbacks)}\n")
    
    # 创建分析器
    analyzer = FeedbackAnalyzer()
    
    # 批量分析
    results = analyzer.analyze_batch(test_feedbacks)
    
    # 输出结果
    print("\n" + "=" * 60)
    print("分析结果")
    print("=" * 60)
    
    for item in results["analysis_results"]:
        print(f"\n【反馈 {item['id']}】{item['original_feedback']}")
        print(f"  类型：{item.get('category', 'N/A')}")
        print(f"  优先级：{item.get('priority', 'N/A')}")
        print(f"  情感：{item.get('sentiment', 'N/A')}")
        print(f"  关键词：{', '.join(item.get('keywords', []))}")
        print(f"  建议：{item.get('suggested_action', 'N/A')}")
    
    print("\n" + "=" * 60)
    print("汇总报告")
    print("=" * 60)
    summary = results["summary"]
    print(f"总处理数：{summary['total']}")
    print(f"正面率：{summary['positive_rate']}%")
    print(f"分类分布：{summary['by_category']}")
    print(f"情感分布：{summary['by_sentiment']}")
    if summary['high_priority_issues']:
        print(f"高优先级问题：{summary['high_priority_issues']}")
    
    # 保存结果
    with open("analysis_result.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存到：analysis_result.json")
    
    return results


if __name__ == "__main__":
    main()
