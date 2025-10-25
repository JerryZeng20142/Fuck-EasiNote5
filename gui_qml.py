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
from PySide6.QtCore import QObject, Signal, Slot, QUrl

from config import config_manager
from utils import find_easinote_path, is_admin

logger = logging.getLogger(__name__)

class Backend(QObject):
    """后端逻辑处理类，连接QML界面和Python逻辑"""
    
    # 信号定义
    statusChanged = Signal(str)
    easiNotePathChanged = Signal(str)
    messageBox = Signal(str, str)  # 标题, 内容
    
    def __init__(self):
        super().__init__()
        self.easinote_path = config_manager.get('paths.easinote_install_path', '')
    
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

def start_qml_gui():
    """启动基于QML的图形界面"""
    logger.info("启动基于RinUI的图形界面")
    
    # 创建应用实例
    app = QGuiApplication(sys.argv)
    
    # 检查是否有RinUI
    if not os.path.exists('RinUI'):
        # 如果没有RinUI文件夹，尝试安装
        logger.warning("未找到RinUI文件夹，尝试从Python包中加载")
    
    # 创建后端实例
    backend = Backend()
    
    # 创建QML引擎
    engine = QQmlApplicationEngine()
    
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
        sys.exit(-1)
    
    # 主循环
    try:
        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"GUI错误: {str(e)}", exc_info=True)
        raise