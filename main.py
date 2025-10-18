#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
希沃白板5修改工具
主要用于修改希沃白板5中的小游戏背景音乐
支持命令行和图形界面两种操作方式
"""

import os
import sys
import argparse
from audio_modifier import AudioModifier
from config import Config
from utils import logger

# 尝试导入GUI模块，如果失败则记录警告
try:
    from gui import run_gui
    GUI_AVAILABLE = True
except ImportError as e:
    logger.warning(f"无法导入GUI模块: {str(e)}")
    GUI_AVAILABLE = False

def parse_arguments():
    """
    解析命令行参数
    
    Returns:
        argparse.Namespace: 解析后的参数命名空间
    """
    parser = argparse.ArgumentParser(description='希沃白板5小游戏背景音乐修改工具')
    parser.add_argument('--cli', action='store_true', help='使用命令行界面')
    parser.add_argument('--gui', action='store_true', help='使用图形界面')
    return parser.parse_args()

def main():
    """
    主程序入口
    根据参数选择启动图形界面或命令行界面
    """
    # 解析命令行参数
    args = parse_arguments()
    
    # 决定启动模式
    # 如果显式指定了--cli，则使用命令行界面
    # 如果显式指定了--gui或未指定参数且GUI可用，则使用图形界面
    use_gui = False
    if args.cli:
        use_gui = False
    elif args.gui or (GUI_AVAILABLE and not args.cli):
        use_gui = True
    
    # 根据模式启动程序
    if use_gui:
        start_gui_mode()
    else:
        start_cli_mode()

def start_gui_mode():
    """
    启动图形界面模式
    """
    if not GUI_AVAILABLE:
        print("错误: 图形界面不可用，请使用命令行界面或检查依赖是否正确安装")
        input("按回车键退出...")
        return
    
    logger.info("启动图形界面模式")
    try:
        run_gui()
    except Exception as e:
        logger.error(f"图形界面运行出错: {str(e)}")
        print(f"错误: 图形界面运行出错: {str(e)}")
        input("按回车键退出...")

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
        print("4. 启动图形界面")
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
            # 启动图形界面
            if GUI_AVAILABLE:
                print("启动图形界面...")
                start_gui_mode()
            else:
                print("错误: 图形界面不可用")
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