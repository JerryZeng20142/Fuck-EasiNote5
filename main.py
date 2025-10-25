#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
希沃白板5修改工具 - Fuck-EasiNote5

一个用于修改希沃白板5软件功能的工具，支持各种自定义设置和功能增强。
"""

import os
import sys
import argparse
import logging
from datetime import datetime

# 设置日志
LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, f'fuck_easinote5_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='希沃白板5修改工具')
    parser.add_argument('--version', action='version', version='Fuck-EasiNote5 v1.0')
    return parser.parse_args()

def main():
    """主函数"""
    args = parse_arguments()
    
    logger.info('Fuck-EasiNote5 启动')
    
    try:
        # 尝试启动基于RinUI的图形界面
        try:
            from gui_qml import start_qml_gui
            start_qml_gui()
        except Exception as qml_error:
            logger.warning(f"无法启动基于RinUI的界面: {str(qml_error)}")
            # 回退到传统的Tkinter界面
            logger.info("回退到传统Tkinter界面")
            from gui import start_gui
            start_gui()
        
    except KeyboardInterrupt:
        logger.info('用户中断操作')
        print("\n程序已退出")
    except Exception as e:
        logger.error(f'程序发生错误: {str(e)}', exc_info=True)
        print(f"错误: {str(e)}")
    finally:
        logger.info('Fuck-EasiNote5 退出')

if __name__ == '__main__':
    main()