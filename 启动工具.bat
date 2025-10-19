@echo off
chcp 65001

echo 欢迎使用希沃白板5修改工具

echo.
echo ============== 工具说明 ==============
echo 本工具支持三种界面模式：
echo 1. 命令行界面 - 兼容性最好，无需额外依赖
echo 2. Tkinter图形界面 - 基础图形界面，系统通常自带

echo 3. Rin-UI图形界面 - 更美观的界面，需要安装额外依赖

echo.--------------------------------------
echo Rin-UI是一个美观的PySide6组件库

echo 更多信息: https://github.com/RinLit-233-shiroko/Rin-UI/

echo =====================================

:menu
echo.
echo ===== 界面模式选择 =====
echo 1. 命令行界面 (兼容性最好)
echo 2. Tkinter图形界面 (基础图形界面)
echo 3. Rin-UI图形界面 (更美观的界面)
echo 4. 安装所有依赖
echo 5. 安装Rin-UI专用依赖
echo 0. 退出
echo ===================

echo.
set /p choice=请输入选择 (0-5): 

if "%choice%" == "1" (
    echo 启动命令行界面...
    python main.py --cli
    goto end
)

if "%choice%" == "2" (
    echo 启动Tkinter图形界面...
    python main.py --gui
    goto end
)

if "%choice%" == "3" (
    echo 启动Rin-UI图形界面...
    echo 请注意：需要安装PySide6和RinUI依赖
    echo 如果启动失败，请先选择选项4或5安装依赖
    python main.py --rin-ui
    goto end
)

if "%choice%" == "4" (
    echo 正在安装所有依赖...
    echo 这将安装Tkinter、PySide6、RinUI等所有必要组件
    pip install -r requirements.txt
    echo 依赖安装完成！
    echo 如果遇到问题，可以尝试：
    echo 1. 以管理员身份运行本脚本
    echo 2. 先更新pip: python -m pip install --upgrade pip
    echo 3. 检查网络连接
    pause
    goto menu
)

if "%choice%" == "5" (
    echo 正在安装Rin-UI专用依赖...
    echo 正在安装: PySide6 和 RinUI
    pip install PySide6 RinUI
    echo Rin-UI依赖安装完成！
    echo 注意：RinUI依赖PySide6，请确保正确安装
    pause
    goto menu
)

if "%choice%" == "0" (
    echo 感谢使用，再见！
    goto end
)

echo 无效的选择，请重新输入！
pause
goto menu

:end
pause