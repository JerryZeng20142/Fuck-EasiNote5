#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置模块
管理希沃白板5修改工具的配置信息
"""

import os
import json
from utils import logger

class Config:
    """
    配置类
    负责配置文件的加载、保存和管理
    """
    
    def __init__(self):
        """
        初始化配置
        加载现有配置或创建默认配置
        """
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
        self.default_config = {
            'easinote_path': 'C:\\Program Files\\Seewo\\EasiNote5',  # 希沃白板5默认安装路径
            'games_dir': 'resources\\games',  # 小游戏相对目录
            'backup_dir': 'backups',  # 备份目录
            'log_level': 'INFO',  # 日志级别
            'audio_formats': ['.mp3', '.wav', '.ogg']  # 支持的音频格式
        }
        
        # 加载配置
        self.config = self._load_config()
        logger.info("配置加载完成")
    
    def _load_config(self):
        """
        加载配置文件
        
        Returns:
            dict: 配置字典
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # 合并默认配置和用户配置
                return {**self.default_config, **config}
            else:
                # 配置文件不存在，返回默认配置
                logger.info("配置文件不存在，使用默认配置")
                return self.default_config.copy()
                
        except Exception as e:
            logger.error(f"加载配置文件时出错: {str(e)}")
            logger.warning("使用默认配置")
            return self.default_config.copy()
    
    def save_config(self):
        """
        保存配置到文件
        
        Returns:
            bool: 是否保存成功
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
            logger.info(f"配置已保存到: {self.config_file}")
            return True
            
        except Exception as e:
            logger.error(f"保存配置文件时出错: {str(e)}")
            return False
    
    def get(self, key, default=None):
        """
        获取配置项
        
        Args:
            key: 配置键名
            default: 默认值
            
        Returns:
            配置值或默认值
        """
        return self.config.get(key, default)
    
    def set(self, key, value):
        """
        设置配置项
        
        Args:
            key: 配置键名
            value: 配置值
        """
        self.config[key] = value
    
    def show_config(self):
        """
        显示当前配置
        """
        print("\n=== 当前配置 ===")
        for key, value in self.config.items():
            print(f"{key}: {value}")
        print("="*30)
    
    def get_games_directory(self):
        """
        获取小游戏目录的完整路径
        
        Returns:
            str: 小游戏目录完整路径
        """
        return os.path.join(self.config['easinote_path'], self.config['games_dir'])