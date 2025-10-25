#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块 - 仅包含图形界面所需的基本功能
"""

import os
import logging
import winreg
import sys
from typing import Optional

logger = logging.getLogger(__name__)

def find_easinote_path() -> Optional[str]:
    """
    自动查找希沃白板5的安装路径
    
    Returns:
        str: 希沃白板5的安装路径，如果未找到则返回None
    """
    try:
        # 尝试从注册表查找
        logger.info("从注册表查找希沃白板安装路径")
        
        # 检查64位注册表
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                               r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
                               0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY) as hkey:
                for i in range(winreg.QueryInfoKey(hkey)[0]):
                    try:
                        key_name = winreg.EnumKey(hkey, i)
                        with winreg.OpenKey(hkey, key_name) as subkey:
                            try:
                                display_name = winreg.QueryValueEx(subkey, 'DisplayName')[0]
                                if '希沃白板' in display_name or 'EasiNote' in display_name:
                                    install_location = winreg.QueryValueEx(subkey, 'InstallLocation')[0]
                                    if os.path.exists(install_location):
                                        return install_location
                            except OSError:
                                continue
                    except OSError:
                        continue
        except OSError:
            pass
        
        # 检查32位注册表
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                               r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
                               0, winreg.KEY_READ | winreg.KEY_WOW64_32KEY) as hkey:
                for i in range(winreg.QueryInfoKey(hkey)[0]):
                    try:
                        key_name = winreg.EnumKey(hkey, i)
                        with winreg.OpenKey(hkey, key_name) as subkey:
                            try:
                                display_name = winreg.QueryValueEx(subkey, 'DisplayName')[0]
                                if '希沃白板' in display_name or 'EasiNote' in display_name:
                                    install_location = winreg.QueryValueEx(subkey, 'InstallLocation')[0]
                                    if os.path.exists(install_location):
                                        return install_location
                            except OSError:
                                continue
                    except OSError:
                        continue
        except OSError:
            pass
        
        # 常见安装路径检查
        common_paths = [
            r'C:\Program Files\Seewo\EasiNote5',
            r'C:\Program Files (x86)\Seewo\EasiNote5',
            r'D:\Program Files\Seewo\EasiNote5',
            r'D:\Program Files (x86)\Seewo\EasiNote5'
        ]
        
        logger.info("检查常见安装路径")
        for path in common_paths:
            if os.path.exists(path):
                logger.info(f"在常见路径找到: {path}")
                return path
        
        logger.warning("未找到希沃白板安装路径")
        return None
        
    except Exception as e:
        logger.error(f"查找希沃白板路径时发生错误: {str(e)}")
        return None

def is_admin() -> bool:
    """
    检查程序是否以管理员权限运行
    
    Returns:
        bool: 是否以管理员权限运行
    """
    try:
        if sys.platform == 'win32':
            # Windows 平台
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            # 非 Windows 平台，检查是否为 root
            return os.geteuid() == 0
    except Exception:
        return False