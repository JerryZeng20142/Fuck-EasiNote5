#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于RinUI和QML的图形界面模块
"""

import os
import sys
import shutil
import logging
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Signal, Slot, QUrl, Property, QFile, QFileInfo, QByteArray
from PySide6.QtWidgets import QFileDialog
import darkdetect

from config import config_manager
from utils import find_easinote_path, find_activities_audios_path, is_admin

logger = logging.getLogger(__name__)

class Backend(QObject):
    """后端逻辑处理类，连接QML界面和Python逻辑，适配RinUI组件"""
    
    # 信号定义
    statusChanged = Signal(str)
    easiNotePathChanged = Signal(str)
    messageBox = Signal(str, str)  # 标题, 内容
    themeChanged = Signal(str)
    resourcesUpdated = Signal()  # 资源列表更新信号
    
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
        # 初始化资源文件夹路径
        self.imported_resources_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imported_resources')
        # 确保资源文件夹存在
        os.makedirs(self.imported_resources_dir, exist_ok=True)
    
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
                
                # 检测到安装路径后，查找活动音频资源路径
                self.statusChanged.emit("正在查找活动音频资源路径...")
                audios_path = find_activities_audios_path()
                if audios_path:
                    config_manager.set('paths.activities_audios_path', audios_path)
                    config_manager.save()
                    self.statusChanged.emit(f"已找到活动音频资源路径: {audios_path}")
                else:
                    self.statusChanged.emit("未找到活动音频资源路径")
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
        """管理资源 - 触发打开资源管理窗口的信号"""
        try:
            self.statusChanged.emit("打开资源管理窗口...")
            # 确保资源文件夹存在
            os.makedirs(self.imported_resources_dir, exist_ok=True)
            self.resourcesUpdated.emit()  # 通知UI资源列表已更新
        except Exception as e:
            logger.error(f"准备资源管理窗口失败: {str(e)}")
            self.messageBox.emit("错误", f"准备资源管理窗口失败: {str(e)}")
    
    @Slot(str, result=bool)
    def importResource(self, filePath):
        """导入资源文件
        
        Args:
            filePath: 文件路径
            
        Returns:
            bool: 导入是否成功
        """
        try:
            self.statusChanged.emit(f"正在导入资源: {os.path.basename(filePath)}")
            
            # 确保资源文件夹存在
            os.makedirs(self.imported_resources_dir, exist_ok=True)
            
            # 获取目标文件路径
            fileName = os.path.basename(filePath)
            destPath = os.path.join(self.imported_resources_dir, fileName)
            
            # 处理文件名冲突
            counter = 1
            baseName, ext = os.path.splitext(fileName)
            while os.path.exists(destPath):
                destPath = os.path.join(self.imported_resources_dir, f"{baseName}_{counter}{ext}")
                counter += 1
            
            # 复制文件
            shutil.copy2(filePath, destPath)
            logger.info(f"资源导入成功: {destPath}")
            
            # 通知资源列表已更新
            self.resourcesUpdated.emit()
            self.statusChanged.emit(f"资源导入成功: {os.path.basename(destPath)}")
            return True
        except Exception as e:
            logger.error(f"导入资源失败: {str(e)}")
            self.messageBox.emit("错误", f"导入资源失败: {str(e)}")
            self.statusChanged.emit("就绪")
            return False
    
    @Slot(str, result=bool)
    def deleteResource(self, fileName):
        """删除资源文件
        
        Args:
            fileName: 文件名
            
        Returns:
            bool: 删除是否成功
        """
        try:
            filePath = os.path.join(self.imported_resources_dir, fileName)
            if os.path.exists(filePath):
                os.remove(filePath)
                logger.info(f"资源删除成功: {fileName}")
                self.resourcesUpdated.emit()  # 通知资源列表已更新
                self.statusChanged.emit(f"资源删除成功: {fileName}")
                return True
            else:
                logger.warning(f"资源文件不存在: {fileName}")
                self.messageBox.emit("警告", "资源文件不存在")
                return False
        except Exception as e:
            logger.error(f"删除资源失败: {str(e)}")
            self.messageBox.emit("错误", f"删除资源失败: {str(e)}")
            return False
    
    @Slot(result='QVariantList')
    def getResourceList(self):
        """获取导入的资源列表
        
        Returns:
            list: 资源文件列表，每个元素包含文件名、大小、修改时间等信息
        """
        try:
            resources = []
            if os.path.exists(self.imported_resources_dir):
                for fileName in os.listdir(self.imported_resources_dir):
                    filePath = os.path.join(self.imported_resources_dir, fileName)
                    if os.path.isfile(filePath):
                        fileInfo = {
                            'name': fileName,
                            'size': os.path.getsize(filePath),
                            'modified': os.path.getmtime(filePath),
                            'path': filePath
                        }
                        resources.append(fileInfo)
            return resources
        except Exception as e:
            logger.error(f"获取资源列表失败: {str(e)}")
            return []
    
    @Slot()
    def openFileDialog(self):
        """打开文件选择对话框"""
        try:
            self.statusChanged.emit("打开文件选择对话框...")
            
            # 创建文件对话框
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            
            # 打开文件选择对话框，允许多选
            files, _ = QFileDialog.getOpenFileNames(
                caption="选择要导入的资源文件",
                dir="",
                filter="所有文件 (*);;音频文件 (*.mp3 *.wav *.ogg *.flac);;图片文件 (*.png *.jpg *.jpeg *.gif)",
                options=options
            )
            
            if files:
                self.statusChanged.emit(f"选择了 {len(files)} 个文件，正在导入...")
                success_count = 0
                for file_path in files:
                    if self.importResource(file_path):
                        success_count += 1
                
                if success_count > 0:
                    self.statusChanged.emit(f"成功导入 {success_count} 个资源文件")
                else:
                    self.statusChanged.emit("就绪")
            else:
                self.statusChanged.emit("就绪")
                
        except Exception as e:
            logger.error(f"打开文件对话框失败: {str(e)}")
            self.statusChanged.emit("就绪")
            self.messageBox.emit("错误", f"无法打开文件对话框: {str(e)}")
    
    @Slot()
    def openResourceFolder(self):
        """打开资源文件夹"""
        try:
            # 确保资源文件夹存在
            os.makedirs(self.imported_resources_dir, exist_ok=True)
            self.statusChanged.emit(f"打开资源文件夹: {self.imported_resources_dir}")
            # 在Windows系统上打开文件夹
            if sys.platform.startswith('win'):
                os.startfile(self.imported_resources_dir)
            # 在macOS上打开文件夹
            elif sys.platform == 'darwin':
                os.system(f'open "{self.imported_resources_dir}"')
            # 在Linux上打开文件夹
            else:
                os.system(f'xdg-open "{self.imported_resources_dir}"')
            self.statusChanged.emit("就绪")
        except Exception as e:
            logger.error(f"打开资源文件夹失败: {str(e)}")
            self.statusChanged.emit("就绪")
            self.messageBox.emit("错误", f"无法打开资源文件夹: {str(e)}")
    
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