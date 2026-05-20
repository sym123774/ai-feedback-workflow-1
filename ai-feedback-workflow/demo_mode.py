"""
演示模式 - 无需 API Key，使用模拟数据展示完整流程
用于面试演示和测试
"""

import json
from datetime import datetime

def analyze_feedback_mock(feedback: str) -> dict:
    """模拟 AI 分析（用于演示）"""
    
    # 关键词匹配规则（简化版）
    feedback_lower = feedback.lower()
    
    # 分类规则
    if any(k in feedback_lower for k in ["慢", "卡", "崩溃", "报错", "bug", "故障"]):
        category = "BUG 投诉"
        priority = "高"
    elif any(k in feedback_lower for k in ["希望", "建议", "增加", "功能"]):
        category = "功能建议"
        priority = "中"
    elif any(k in feedback_lower for k in ["好", "棒", "漂亮", "满意", "感谢"]):
        category = "表扬感谢"
        priority = "低"
    elif any(k in feedback_lower for k in ["怎么", "如何", "哪里", "为什么"]):
        category = "使用咨询"
        priority = "中"
    else:
        category = "其他"
        priority = "中"
    
    # 情感分析
    if any(k in feedback_lower for k in ["太", "差", "慢", "烦", "失望", "投诉"]):
        sentiment = "负面"
    elif any(k in feedback_lower for k in ["好", "棒", "满意", "感谢", "喜欢"]):
        sentiment = "正面"
    else:
        sentiment = "中性"
    
    # 关键词提取（简化）
    keywords = []
    if "慢" in feedback or "卡" in feedback:
        keywords.append("性能优化")
    if "功能" in feedback:
        keywords.append("功能需求")
    if "界面" in feedback or "设计" in feedback:
        keywords.append("UI 设计")
    if "客服" in feedback:
        keywords.append("客户服务")
    if not keywords:
        keywords = ["一般反馈"]
    
    # 建议动作
    actions = {
        "BUG 投诉": "技术团队优先排查",
        "功能建议": "产品评估需求，排期开发",
        "表扬感谢": "同步团队，保持优点",
        "使用咨询": "客服及时响应",
        "其他": "人工复核分类"
    }
    
    return {
        "category": category,
        "priority": priority,
        "sentiment": sentiment,
        "keywords": keywords,
        "summary": f"用户反馈{category}，情感{sentiment}",
        "suggested_action": actions.get(category, "人工处理")
    }


def main():
    """演示模式主函数"""
    print("=" * 70)
    print("AI 用户反馈智能分析工作流 - 演示模式")
    print("=" * 70)
    print(f"运行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("注意：此为演示模式，使用模拟数据")
    print("=" * 70)
    
    # 测试样例
    test_feedbacks = [
        "APP 打开太慢了，希望能优化一下启动速度",
        "新增的深色模式很好用！但是希望能自定义主题颜色",
        "客服响应太慢，问题三天了还没解决",
        "这个功能完全没法用，一直报错 500",
        "界面设计很漂亮，用户体验不错",
        "希望能增加导出 Excel 的功能，现在只能截图",
    ]
    
    print(f"\n待分析反馈：{len(test_feedbacks)} 条\n")
    
    results = []
    for i, feedback in enumerate(test_feedbacks, 1):
        print(f"--- 反馈 {i} ---")
        print(f"输入：{feedback}")
        
        analysis = analyze_feedback_mock(feedback)
        analysis["id"] = i
        analysis["original_feedback"] = feedback
        
        print(f"输出：{json.dumps(analysis, ensure_ascii=False, indent=2)}")
        print()
        
        results.append(analysis)
    
    # 生成汇总
    summary = {
        "total": len(results),
        "by_category": {},
        "by_sentiment": {"正面": 0, "中性": 0, "负面": 0},
        "high_priority": []
    }
    
    for r in results:
        # 分类统计
        cat = r["category"]
        summary["by_category"][cat] = summary["by_category"].get(cat, 0) + 1
        
        # 情感统计
        summary["by_sentiment"][r["sentiment"]] += 1
        
        # 高优先级
        if r["priority"] == "高":
            summary["high_priority"].append(r["summary"])
    
    print("=" * 70)
    print("汇总报告")
    print("=" * 70)
    print(f"总处理数：{summary['total']}")
    print(f"分类分布：{json.dumps(summary['by_category'], ensure_ascii=False)}")
    print(f"情感分布：{summary['by_sentiment']}")
    print(f"高优先级问题：{summary['high_priority']}")
    
    # 保存结果
    output = {
        "timestamp": datetime.now().isoformat(),
        "mode": "demo",
        "analysis_results": results,
        "summary": summary
    }
    
    with open("demo_output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n结果已保存到：demo_output.json")
    print("\n" + "=" * 70)
    print("演示完成！")
    print("=" * 70)
    
    return output


if __name__ == "__main__":
    main()
