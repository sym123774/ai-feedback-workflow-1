"""
AI 用户反馈智能分析工作流（MVP 最终版）
✅ 命令行运行
✅ 3组不同输入自动切换
✅ 结构化JSON输出
✅ 无需API 无需改代码
"""
import json
import random

# 3组测试用例（自动轮换，不用改代码）
TEST_CASES = [
    # 第1组：混合反馈
    [
        "APP打开太慢，希望优化启动速度",
        "深色模式很好用，希望自定义颜色",
        "客服响应太慢，问题三天没解决",
        "功能报错无法使用",
        "界面很漂亮，体验不错",
        "希望增加导出Excel功能"
    ],
    # 第2组：纯BUG负面
    [
        "软件总是闪退，文件丢失",
        "登录失败收不到验证码",
        "界面卡顿操作延迟高",
        "上传文件一直失败",
        "按钮无响应功能瘫痪",
        "更新后黑屏打不开"
    ],
    # 第3组：好评+建议
    [
        "软件非常好用，界面简洁流畅",
        "希望增加批量导出PDF功能",
        "夜间模式舒服，希望多配色",
        "体验很好，推荐使用",
        "希望支持云端同步",
        "启动速度快，非常满意"
    ]
]

def analyze(feedback):
    """离线智能分析"""
    if any(k in feedback for k in ["闪退","报错","失败","卡","慢","黑屏","打不开"]):
        return {"类型":"BUG投诉","优先级":"高","情感":"负面","关键词":"故障,异常","建议":"紧急修复"}
    elif any(k in feedback for k in ["希望","增加","优化","导出","自定义"]):
        return {"类型":"功能建议","优先级":"中","情感":"中性","关键词":"需求,优化","建议":"纳入规划"}
    elif any(k in feedback for k in ["好用","不错","漂亮","满意","流畅"]):
        return {"类型":"表扬感谢","优先级":"低","情感":"正面","关键词":"好评,体验","建议":"保持优化"}
    elif "客服" in feedback:
        return {"类型":"服务投诉","优先级":"高","情感":"负面","关键词":"客服,效率","建议":"优化流程"}
    else:
        return {"类型":"其他","优先级":"中","情感":"中性","关键词":"常规","建议":"常规跟进"}

def run_workflow():
    print("="*50)
    print("AI 用户反馈智能分析工作流 ✅ 命令行版")
    print("="*50)

    # 自动选组：运行第几次就用第几组
    run_num = int(input("输入运行次数（1/2/3）："))-1
    feedbacks = TEST_CASES[run_num]

    print(f"\n▶  第{run_num+1}组数据，共{len(feedbacks)}条反馈\n")

    results = []
    for i, f in enumerate(feedbacks,1):
        res = analyze(f)
        results.append({"id":i,"内容":f,**res})
        print(f"【反馈{i}】{f}")
        print(f"  类型:{res['类型']}  优先级:{res['优先级']}  情感:{res['情感']}")
        print(f"  关键词:{res['关键词']}  建议:{res['建议']}\n")

    # 汇总
    total = len(results)
    bug = len([r for r in results if "BUG" in r["类型"] or "服务" in r["类型"]])
    good = len([r for r in results if r["情感"]=="正面"])
    summary = {
        "总数量":total, "BUG/投诉":bug, "正面反馈":good,
        "高优先级": [r["内容"] for r in results if r["优先级"]=="高"][:3]
    }

    print("="*30+" 汇总报告 "+"="*30)
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    # 保存JSON
    with open(f"result_{run_num+1}.json","w",encoding="utf-8") as f:
        json.dump({"分析结果":results,"汇总":summary},f,ensure_ascii=False,indent=2)
    
    print(f"\n✅ 结果已保存：result_{run_num+1}.json")

if __name__ == "__main__":
    run_workflow()
    