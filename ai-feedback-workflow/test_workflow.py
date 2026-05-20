"""
测试脚本 - 验证工作流功能
"""

import json
from ai_workflow import FeedbackAnalyzer

def test_workflow():
    """测试工作流"""
    print("=" * 60)
    print("AI 反馈分析工作流 - 测试")
    print("=" * 60)
    
    # 加载测试样例
    with open("test_samples.json", "r", encoding="utf-8") as f:
        test_data = json.load(f)
    
    feedbacks = test_data["feedback_list"]
    print(f"\n测试样例数量：{len(feedbacks)}\n")
    
    # 创建分析器
    analyzer = FeedbackAnalyzer()
    
    # 测试前 3 条（展示用）
    print("测试前 3 条反馈：\n")
    
    for i, feedback in enumerate(feedbacks[:3], 1):
        print(f"--- 测试样例 {i} ---")
        print(f"输入：{feedback}\n")
        
        result = analyzer.analyze_single_feedback(feedback)
        
        print("输出:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print()
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
    
    # 保存测试结果
    with open("test_output.json", "w", encoding="utf-8") as f:
        json.dump({
            "test_samples": feedbacks[:3],
            "results": [analyzer.analyze_single_feedback(f) for f in feedbacks[:3]]
        }, f, ensure_ascii=False, indent=2)
    
    print("测试结果已保存到：test_output.json")


if __name__ == "__main__":
    test_workflow()
