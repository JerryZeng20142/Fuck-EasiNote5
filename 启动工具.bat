@echo off
REM 希沃白板5修改工具启动脚本

cls
echo 正在启动希沃白板5修改工具...
echo =====================================

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python。请确保已安装Python 3.6或更高版本。
    pause
    exit /b 1
)

REM 尝试启动图形界面版本
echo 启动图形界面版本...
python main.py

REM 如果图形界面启动失败，尝试命令行版本
if %errorlevel% neq 0 (
    echo 图形界面启动失败，尝试命令行版本...
    python main.py --cli
)

pause