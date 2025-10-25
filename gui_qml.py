#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于RinUI和QML的图形界面模块
"""

import os
import sys
import logging
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Signal, Slot, QUrl, Property
import darkdetect

from config import config_manager
from utils import find_easinote_path, is_admin

logger = logging.getLogger(__name__)

class Backend(QObject):
    """后端逻辑处理类，连接QML界面和Python逻辑，适配RinUI组件"""
    
    # 信号定义
    statusChanged = Signal(str)
    easiNotePathChanged = Signal(str)
    messageBox = Signal(str, str)  # 标题, 内容
    themeChanged = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.easinote_path = config_manager.get('paths.easinote_install_path', '')
        # 检测系统主题并设置默认主题
        self._dark_mode = darkdetect.isDark()
        # 获取或设置主题配置
        current_theme = config_manager.get('gui.theme', '')
        if not current_theme:
            config_manager.set('gui.theme', 'dark' if self._dark_mode else 'light')
            config_manager.save()
    
    # 属性定义
    @Property(bool, notify=themeChanged)
    def isDarkMode(self):
        """获取当前是否为深色模式"""
        return self._dark_mode
    
    @Property(str, notify=themeChanged)
    def theme(self):
        """获取当前主题名称"""
        return config_manager.get('gui.theme', 'light')
    
    @theme.setter
    def theme(self, value):
        """设置主题"""
        if value in ["light", "dark"]:
            self._dark_mode = value == "dark"
            config_manager.set('gui.theme', value)
            config_manager.save()
            self.themeChanged.emit(value)
    
    @Slot(str)
    def setEasiNotePath(self, path):
        """设置希沃白板路径"""
        self.easinote_path = path
        config_manager.set('paths.easinote_install_path', path)
        config_manager.save()
    
    @Slot(result=str)
    def getEasiNotePath(self):
        """获取希沃白板路径"""
        return self.easinote_path
    
    @Slot()
    def autoDetectEasiNote(self):
        """自动检测希沃白板安装路径"""
        self.statusChanged.emit("正在检测希沃白板安装路径...")
        
        try:
            path = find_easinote_path()
            if path:
                self.easinote_path = path
                self.easiNotePathChanged.emit(path)
                config_manager.set('paths.easinote_install_path', path)
                config_manager.save()
                self.statusChanged.emit(f"已找到希沃白板安装路径: {path}")
            else:
                self.messageBox.emit("未找到", "无法自动检测希沃白板安装路径，请手动选择")
                self.statusChanged.emit("就绪")
        except Exception as e:
            logger.error(f"自动检测失败: {str(e)}")
            self.messageBox.emit("错误", f"自动检测失败: {str(e)}")
            self.statusChanged.emit("就绪")
    
    @Slot(str, result=str)
    def getConfigValue(self, key):
        """获取配置值"""
        return config_manager.get(key, '')
    
    @Slot(str, str)
    def setConfigValue(self, key, value):
        """设置配置值"""
        config_manager.set(key, value)
        config_manager.save()
    
    @Slot()
    def createBackup(self):
        """创建备份"""
        self.messageBox.emit("提示", "备份功能正在开发中")
    
    @Slot()
    def applyModifications(self):
        """应用修改"""
        self.messageBox.emit("提示", "修改功能正在开发中")
    
    @Slot()
    def restoreOriginal(self):
        """恢复原始文件"""
        self.messageBox.emit("提示", "恢复功能正在开发中")
    
    @Slot(result=bool)
    def checkAdminRights(self):
        """检查是否有管理员权限"""
        return is_admin()
    
    @Slot()
    def toggleTheme(self):
        """切换主题模式"""
        self._dark_mode = not self._dark_mode
        new_theme = "dark" if self._dark_mode else "light"
        config_manager.set('gui.theme', new_theme)
        config_manager.save()
        self.themeChanged.emit(new_theme)
        self.statusChanged.emit(f"主题已切换为: {new_theme}")
    
    @Slot()
    def optimizeStartup(self):
        """执行启动项优化"""
        self.statusChanged.emit("启动项优化功能开发中...")
        self.messageBox.emit("提示", "启动项优化功能开发中")
    
    @Slot()
    def simplifyUI(self):
        """执行界面精简"""
        self.statusChanged.emit("界面精简功能开发中...")
        self.messageBox.emit("提示", "界面精简功能开发中")
    
    @Slot()
    def manageResources(self):
        """管理资源"""
        self.statusChanged.emit("资源管理功能开发中...")
        self.messageBox.emit("提示", "资源管理功能开发中")
    
    @Slot()
    def backupSettings(self):
        """备份设置"""
        self.statusChanged.emit("设置备份功能开发中...")
        self.messageBox.emit("提示", "设置备份功能开发中")
    
    @Slot()
    def restoreSettings(self):
        """恢复设置"""
        self.statusChanged.emit("设置恢复功能开发中...")
        self.messageBox.emit("提示", "设置恢复功能开发中")

def start_qml_gui():
    """启动基于QML的图形界面"""
    logger.info("启动基于RinUI的图形界面")
    
    # 创建应用实例
    app = QGuiApplication(sys.argv)
    
    # 检查是否有RinUI组件
    # 现在RinUI在项目根目录下
    rinu_dir = 'RinUI'
    if not os.path.exists(rinu_dir):
        # 如果没有RinUI文件夹，尝试从Python包中加载
        logger.warning(f"未找到RinUI组件目录: {rinu_dir}，尝试从Python包中加载")
    else:
        logger.info(f"找到RinUI组件目录: {rinu_dir}")
    
    # 创建后端实例
    backend = Backend()
    
    # 创建QML引擎
    engine = QQmlApplicationEngine()
    
    # 添加RinUI到QML导入路径
    # 确保RinUI可以被正确导入
    qml_import_path = os.path.abspath(rinu_dir)
    engine.addImportPath(qml_import_path)
    logger.info(f"已添加QML导入路径: {qml_import_path}")
    
    # 注册后端到QML
    engine.rootContext().setContextProperty("backend", backend)
    
    # 加载主QML文件
    qml_file = os.path.join("ui", "main.qml")
    if os.path.exists(qml_file):
        engine.load(QUrl.fromLocalFile(qml_file))
    else:
        # 如果没有找到QML文件，使用默认的简单界面
        logger.warning(f"未找到QML文件: {qml_file}，使用默认界面")
        
        # 创建临时QML内容
        default_qml = '''
        import QtQuick 2.15
        import QtQuick.Window 2.15
        import QtQuick.Controls 2.15
        
        Window {
            visible: true
            width: 800
            height: 600
            title: "希沃白板5修改工具"
            
            Rectangle {
                anchors.fill: parent
                color: "#f0f0f0"
                
                Column {
                    anchors.centerIn: parent
                    spacing: 20
                    
                    Text {
                        text: "希沃白板5修改工具"
                        font.pointSize: 24
                        font.bold: true
                        color: "#333"
                    }
                    
                    Text {
                        text: "请确保在ui目录下有main.qml文件"
                        color: "#666"
                    }
                    
                    Text {
                        text: "RinUI 正在配置中..."
                        color: "#666"
                    }
                }
            }
        }
        '''
        
        # 保存临时QML文件
        os.makedirs("ui", exist_ok=True)
        with open(qml_file, "w", encoding="utf-8") as f:
            f.write(default_qml)
        
        engine.load(QUrl.fromLocalFile(qml_file))
    
    # 检查是否有根对象
    if not engine.rootObjects():
        logger.error("无法加载QML界面")
        # 抛出异常而不是直接退出，让main.py可以捕获并回退到Tkinter界面
        raise RuntimeError("无法加载QML界面")
    
    # 主循环
    try:
        # 不使用sys.exit，而是返回退出码
        return app.exec()
    except Exception as e:
        logger.error(f"GUI错误: {str(e)}", exc_info=True)
        raise