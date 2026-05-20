@echo off
chcp 65001 >nul
echo ========================================
echo AI 用户反馈智能分析工作流 - 快速测试
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 检查 Python 环境...
python --version
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo.
echo [2/3] 检查依赖包...
python -c "import requests; import dotenv" 2>nul
if errorlevel 1 (
    echo [提示] 正在安装依赖...
    pip install -r requirements.txt
) else (
    echo [完成] 依赖包已安装
)

echo.
echo [3/3] 运行测试...
echo.
python test_workflow.py

echo.
echo ========================================
echo 测试完成！
echo 查看结果：test_output.json
echo ========================================
pause
