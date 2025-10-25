#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
"""

import os
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# 默认配置
DEFAULT_CONFIG = {
    'app': {
        'name': 'Fuck-EasiNote5',
        'version': '1.0',
        'author': 'Unknown'
    },
    'paths': {
        'easinote_install_path': ''
    },
    'gui': {
        'theme': 'light',
        'language': 'zh_CN',
        'window_size': [800, 600]
    }
}

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = 'config.json'):
        self.config_file = config_file
        self.config: Dict[str, Any] = DEFAULT_CONFIG.copy()
        self.load()
        
    def load(self) -> None:
        """从文件加载配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    self._merge_config(DEFAULT_CONFIG, user_config)
                    logger.info('配置已加载')
            else:
                logger.info('配置文件不存在，使用默认配置')
                self.save()
        except Exception as e:
            logger.error(f'加载配置失败: {str(e)}')
            self.config = DEFAULT_CONFIG.copy()
    
    def save(self) -> None:
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            logger.info('配置已保存')
        except Exception as e:
            logger.error(f'保存配置失败: {str(e)}')
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any) -> None:
        """设置配置值"""
        keys = key_path.split('.')
        config = self.config
        
        # 遍历到倒数第二个键
        for key in keys[:-1]:
            if key not in config or not isinstance(config[key], dict):
                config[key] = {}
            config = config[key]
        
        # 设置最后一个键的值
        config[keys[-1]] = value
    
    def _merge_config(self, base: Dict[str, Any], update: Dict[str, Any]) -> None:
        """递归合并配置"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

# 创建全局配置实例
config_manager = ConfigManager()