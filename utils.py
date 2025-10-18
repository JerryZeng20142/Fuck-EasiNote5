#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具模块
提供希沃白板5修改工具所需的通用功能
"""

import os
import logging
from datetime import datetime

# 配置日志
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"easinote_tool_{datetime.now().strftime('%Y%m%d')}.log")

# 创建logger实例
logger = logging.getLogger('easinote_tool')
logger.setLevel(logging.DEBUG)  # 设置最低日志级别

# 创建文件处理器
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.INFO)  # 文件日志级别

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # 控制台日志级别

# 设置日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 添加处理器到logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def ensure_directory(path):
    """
    确保目录存在，如果不存在则创建
    
    Args:
        path: 目录路径
    """
    os.makedirs(path, exist_ok=True)
    logger.debug(f"确保目录存在: {path}")


def get_file_list(directory, extensions=None):
    """
    获取目录下指定扩展名的文件列表
    
    Args:
        directory: 目录路径
        extensions: 文件扩展名列表，如['.mp3', '.wav']
        
    Returns:
        list: 文件路径列表
    """
    file_list = []
    
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if extensions:
                    if any(file.lower().endswith(ext) for ext in extensions):
                        file_list.append(os.path.join(root, file))
                else:
                    file_list.append(os.path.join(root, file))
        
        logger.debug(f"在目录 {directory} 中找到 {len(file_list)} 个文件")
        return file_list
        
    except Exception as e:
        logger.error(f"获取文件列表时出错: {str(e)}")
        return []


def is_valid_path(path):
    """
    检查路径是否有效
    
    Args:
        path: 要检查的路径
        
    Returns:
        bool: 路径是否有效
    """
    try:
        return os.path.exists(path)
    except Exception as e:
        logger.error(f"检查路径有效性时出错: {str(e)}")
        return False


def get_file_info(file_path):
    """
    获取文件信息
    
    Args:
        file_path: 文件路径
        
    Returns:
        dict: 文件信息字典，包含文件名、大小、修改时间等
    """
    try:
        if not os.path.exists(file_path):
            return None
        
        stats = os.stat(file_path)
        return {
            'name': os.path.basename(file_path),
            'path': file_path,
            'size': stats.st_size,  # 字节
            'size_mb': round(stats.st_size / (1024 * 1024), 2),  # MB
            'modified': datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        }
        
    except Exception as e:
        logger.error(f"获取文件信息时出错: {str(e)}")
        return None


def format_bytes(bytes_value):
    """
    格式化字节数为人类可读的格式
    
    Args:
        bytes_value: 字节数
        
    Returns:
        str: 格式化后的字符串
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_value < 1024 or unit == 'GB':
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024