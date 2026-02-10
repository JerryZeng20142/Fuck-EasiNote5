import json
import os
from pathlib import Path

class ConfigManager:
    """
    配置管理类，用于保存和加载配置信息
    """
    
    def __init__(self, config_file="config.json"):
        """
        初始化配置管理器
        
        参数：
            config_file: 配置文件路径，默认为config.json
        """
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self):
        """
        从配置文件加载配置
        
        返回：
            dict: 配置字典
        """
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}
    
    def save_config(self):
        """
        将配置保存到文件
        """
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)
    
    def get(self, key, default=None):
        """
        获取配置项
        
        参数：
            key: 配置键
            default: 默认值
            
        返回：
            配置值或默认值
        """
        return self.config.get(key, default)
    
    def set(self, key, value):
        """
        设置配置项
        
        参数：
            key: 配置键
            value: 配置值
        """
        self.config[key] = value
        self.save_config()
    
    def get_easinote_path(self):
        """
        获取希沃白板安装路径
        
        返回：
            str: 希沃白板安装路径
        """
        return self.get("easinote_path", "")
    
    def set_easinote_path(self, path):
        """
        设置希沃白板安装路径
        
        参数：
            path: 希沃白板安装路径
        """
        self.set("easinote_path", path)
    
    def get_theme(self):
        """
        获取主题设置
        
        返回：
            str: 主题名称（"auto", "dark", "light"），默认"auto"
        """
        return self.get("theme", "auto")
    
    def set_theme(self, theme):
        """
        设置主题
        
        参数：
            theme: 主题名称（"auto", "dark", "light"）
        """
        self.set("theme", theme)
