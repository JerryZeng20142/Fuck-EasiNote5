#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
希沃白板5修改工具
主要用于修改希沃白板5中的小游戏背景音乐
支持命令行、Tkinter图形界面和Rin-UI图形界面三种操作方式
"""

import os
import sys
import argparse
import traceback
from audio_modifier import AudioModifier
from config import Config
from utils import logger

# 移除Tkinter GUI支持
TK_GUI_AVAILABLE = False

# 尝试导入Rin-UI模块，如果失败则记录警告及安装指导
try:
    from gui_rin import run_rin_ui
    RIN_GUI_AVAILABLE = True
except ImportError as e:
    logger.warning(f"无法导入Rin-UI模块: {str(e)}")
    logger.warning("请尝试安装依赖: pip install PySide6 RinUI")
    RIN_GUI_AVAILABLE = False

def parse_arguments():
    """
    解析命令行参数
    
    Returns:
        argparse.Namespace: 解析后的参数命名空间
    """
    parser = argparse.ArgumentParser(description='希沃白板5小游戏背景音乐修改工具')
    parser.add_argument('--cli', action='store_true', help='使用命令行界面')
    parser.add_argument('--gui', action='store_true', help='使用Tkinter图形界面')
    parser.add_argument('--rin-ui', action='store_true', help='使用Rin-UI图形界面')
    return parser.parse_args()

def check_dependencies():
    """
    检查必要的依赖是否安装
    
    Returns:
        bool: 依赖是否满足
    """
    logger.info("检查必要依赖...")
    try:
        # 检查核心依赖
        import json
        import zipfile
        import shutil
        logger.info("核心依赖检查通过")
        return True
    except ImportError as e:
        logger.error(f"核心依赖缺失: {e}")
        return False

def run_cli_mode():
    """
    运行命令行模式
    
    Returns:
        bool: 是否成功运行
    """
    try:
        # 直接调用命令行模式的启动函数
        start_cli_mode()
        return True
    except Exception as e:
        logger.error(f"命令行界面运行出错: {e}")
        traceback.print_exc()
        return False

def run_tkinter_gui():
    """
    运行Tkinter图形界面（已移除）
    
    Returns:
        bool: 是否成功运行
    """
    logger.warning("Tkinter GUI支持已移除")
    return False

def run_rin_ui_gui():
    """
    运行Rin-UI图形界面
    
    Returns:
        bool: 是否成功运行
    """
    try:
        # 直接调用Rin-UI的run_rin_ui函数
        if RIN_GUI_AVAILABLE:
            result = run_rin_ui()
            # 如果run_rin_ui有返回值，则根据返回码判断是否成功
            # 否则默认为True
            return result == 0 if result is not None else True
        else:
            logger.warning("Rin-UI不可用")
            # 显示安装指导
            print("提示: 请安装Rin-UI依赖来使用此界面模式")
            print("安装命令: pip install PySide6 RinUI")
            return False
    except Exception as e:
        logger.error(f"Rin-UI图形界面运行出错: {e}")
        traceback.print_exc()
        # 显示错误和安装指导
        print(f"错误: Rin-UI图形界面运行出错: {str(e)}")
        print("请尝试重新安装依赖: pip install -U PySide6 RinUI")
        return False

def main():
    """
    主程序入口
    根据参数选择启动命令行界面、Tkinter图形界面或Rin-UI图形界面
    改进的界面模式切换逻辑，确保能正确启动Rin-UI界面
    """
    logger.info("希沃白板5修改工具启动")
    
    # 检查核心依赖
    if not check_dependencies():
        print("错误: 核心依赖缺失，请安装必要的Python库")
        input("按回车键退出...")
        sys.exit(1)
    
    # 解析命令行参数
    args = parse_arguments()
    
    # 根据参数选择界面模式
    if args.cli:
        # 命令行模式
        if not run_cli_mode():
            print("命令行界面启动失败")
            input("按回车键退出...")
            sys.exit(1)
    elif args.gui:
        # Tkinter图形界面模式（已移除）
        print("错误: Tkinter图形界面支持已移除")
        input("按回车键退出...")
        sys.exit(1)
    elif args.rin_ui:
        # Rin-UI图形界面模式
        if not run_rin_ui_gui():
            print("Rin-UI图形界面启动失败，尝试Tkinter图形界面...")
            if not run_tkinter_gui():
                print("Tkinter图形界面启动失败，尝试命令行界面...")
                if not run_cli_mode():
                    input("按回车键退出...")
                    sys.exit(1)
    else:
        # 默认模式：尝试启动Rin-UI界面，如果不可用则直接使用命令行
        logger.info("尝试启动默认界面(优先Rin-UI)")
        
        # 首先尝试Rin-UI
        if RIN_GUI_AVAILABLE and run_rin_ui_gui():
            logger.info("Rin-UI界面正常退出")
            return
        else:
            logger.warning("Rin-UI界面不可用或启动失败")
            
        # 直接降级到命令行
        if run_cli_mode():
            logger.info("命令行界面正常退出")
            return
        else:
            logger.error("所有界面模式启动失败")
            print("错误: 无法启动任何界面模式，请检查依赖安装")
            input("按回车键退出...")
            sys.exit(1)

def start_gui_mode():
    """
    启动Tkinter图形界面模式（已移除）
    """
    print("错误: Tkinter图形界面支持已移除")
    input("按回车键退出...")

def start_rin_ui_mode():
    """
    启动Rin-UI图形界面模式
    
    Returns:
        int: 程序退出码
    """
    if not RIN_GUI_AVAILABLE:
        print("错误: Rin-UI图形界面不可用")
        print("请按以下步骤安装必要的依赖:")
        print("1. 确保已安装Python 3.7或更高版本")
        print("2. 运行命令: pip install PySide6 RinUI")
        print("3. 如果遇到问题，尝试更新pip: python -m pip install --upgrade pip")
        print("4. 或者使用requirements.txt: pip install -r requirements.txt")
        input("按回车键退出...")
        return 1
    
    logger.info("启动Rin-UI图形界面模式")
    try:
        # 调用run_rin_ui并返回其返回值
        return run_rin_ui()
    except ImportError as e:
        logger.error(f"导入Rin-UI模块时出错: {str(e)}")
        print(f"错误: 导入Rin-UI模块时出错: {str(e)}")
        print("这可能是由于Rin-UI库安装不完整导致的")
        print("请尝试重新安装: pip install -U PySide6 RinUI")
        input("按回车键退出...")
        return 1
    except Exception as e:
        logger.error(f"Rin-UI图形界面运行出错: {str(e)}")
        print(f"错误: Rin-UI图形界面运行出错: {str(e)}")
        print("请检查错误信息并尝试解决问题")
        input("按回车键退出...")
        return 1

def start_cli_mode():
    """
    启动命令行界面模式
    """
    print("===== 希沃白板5修改工具 =====")
    print("功能：修改希沃白板5小游戏背景音乐")
    print("作者：某中学生叫姐姐Jerry")
    print("版本：0.1.0")
    print("="*30)
    print("提示: 可以使用 --gui 参数启动图形界面")
    print("="*30)
    
    try:
        # 加载配置
        config = Config()
        
        # 初始化音频修改器
        modifier = AudioModifier(config)
        
        # 显示菜单
        show_menu(modifier, config)
        
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        input("按回车键退出...")

def show_menu(modifier, config):
    """
    显示主菜单
    """
    while True:
        print("\n请选择操作：")
        print("1. 修改小游戏背景音乐")
        print("2. 恢复默认背景音乐")
        print("3. 查看当前配置")
        print("4. 启动Rin-UI图形界面")
        print("5. 退出")
        
        choice = input("请输入选择 (1-5): ").strip()
        
        if choice == '1':
            # 修改背景音乐
            modify_bgm(modifier)
        elif choice == '2':
            # 恢复默认背景音乐
            restore_bgm(modifier)
        elif choice == '3':
            # 查看当前配置
            config.show_config()
        elif choice == '4':
            # 启动Rin-UI图形界面
            if RIN_GUI_AVAILABLE:
                print("启动Rin-UI图形界面...")
                start_rin_ui_mode()
            else:
                print("错误: Rin-UI图形界面不可用")
                print("尝试安装: pip install PySide6 RinUI")
        elif choice == '5':
            # 退出程序
            print("感谢使用，再见！")
            break
        else:
            print("无效的选择，请重新输入！")

def modify_bgm(modifier):
    """
    修改背景音乐
    """
    print("\n=== 修改背景音乐 ===")
    # 这里将实现背景音乐修改的具体逻辑
    print("功能开发中...")

def restore_bgm(modifier):
    """
    恢复默认背景音乐
    """
    print("\n=== 恢复默认背景音乐 ===")
    # 这里将实现恢复默认背景音乐的具体逻辑
    print("功能开发中...")

if __name__ == "__main__":
    main()