#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图形界面模块
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import logging

from config import config_manager
from utils import find_easinote_path, is_admin

logger = logging.getLogger(__name__)

class EasiNoteModifierGUI:
    """希沃白板修改工具图形界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(f"{config_manager.get('app.name')} v{config_manager.get('app.version')}")
        
        # 设置窗口大小
        window_size = config_manager.get('gui.window_size', [800, 600])
        self.root.geometry(f"{window_size[0]}x{window_size[1]}")
        self.root.minsize(600, 400)
        
        # 检查是否以管理员权限运行
        if not is_admin():
            messagebox.showwarning("权限警告", "建议以管理员权限运行此程序以确保所有功能正常工作")
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标签页
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建各个标签页
        self.create_main_tab()
        self.create_features_tab()
        self.create_settings_tab()
        self.create_about_tab()
        
        # 创建状态栏
        self.status_var = tk.StringVar(value="就绪")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def create_main_tab(self):
        """创建主标签页"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="主界面")
        
        # 希沃白板路径设置
        path_frame = ttk.LabelFrame(tab, text="希沃白板安装路径", padding="10")
        path_frame.pack(fill=tk.X, pady=5)
        
        self.path_var = tk.StringVar(value=config_manager.get('paths.easinote_install_path', ''))
        path_entry = ttk.Entry(path_frame, textvariable=self.path_var, width=50)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        browse_btn = ttk.Button(path_frame, text="浏览...", command=self.browse_easinote_path)
        browse_btn.pack(side=tk.RIGHT, padx=5)
        
        auto_detect_btn = ttk.Button(path_frame, text="自动检测", command=self.auto_detect_easinote)
        auto_detect_btn.pack(side=tk.RIGHT, padx=5)
        
        # 操作按钮
        actions_frame = ttk.Frame(tab, padding="10")
        actions_frame.pack(fill=tk.X, pady=20)
        
        backup_btn = ttk.Button(actions_frame, text="创建备份", command=self.create_backup)
        backup_btn.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        
        apply_btn = ttk.Button(actions_frame, text="应用修改", command=self.apply_modifications)
        apply_btn.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        
        restore_btn = ttk.Button(actions_frame, text="恢复原始", command=self.restore_original)
        restore_btn.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
    
    def create_features_tab(self):
        """创建功能标签页"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="功能修改")
        
        # 简化的功能页面
        info_frame = ttk.Frame(tab, padding="20")
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(info_frame, text="功能修改模块正在开发中...", font=('Arial', 12)).pack(pady=20)
        ttk.Label(info_frame, text="请稍后再试。").pack(pady=10)
    
    def create_settings_tab(self):
        """创建设置标签页"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="设置")
        
        # 主题设置
        theme_frame = ttk.LabelFrame(tab, text="界面设置", padding="10")
        theme_frame.pack(fill=tk.X, pady=5)
        
        theme_label = ttk.Label(theme_frame, text="主题:")
        theme_label.pack(side=tk.LEFT, padx=5)
        
        self.theme_var = tk.StringVar(value=config_manager.get('gui.theme', 'light'))
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var, values=['light', 'dark'])
        theme_combo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 保存设置按钮
        save_btn = ttk.Button(tab, text="保存设置", command=self.save_settings)
        save_btn.pack(pady=20)
    
    def create_about_tab(self):
        """创建关于标签页"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="关于")
        
        about_frame = ttk.Frame(tab, padding="20")
        about_frame.pack(fill=tk.BOTH, expand=True)
        
        app_name = config_manager.get('app.name', 'Fuck-EasiNote5')
        app_version = config_manager.get('app.version', '1.0')
        app_author = config_manager.get('app.author', 'Unknown')
        
        ttk.Label(about_frame, text=app_name, font=('Arial', 16, 'bold')).pack(pady=10)
        ttk.Label(about_frame, text=f"版本: {app_version}").pack(pady=5)
        ttk.Label(about_frame, text=f"作者: {app_author}").pack(pady=5)
        ttk.Label(about_frame, text="希沃白板5修改工具，支持各种自定义设置和功能增强。").pack(pady=10)
        ttk.Label(about_frame, text="使用此工具风险自负，请确保备份原始文件。").pack(pady=5)
    
    def browse_easinote_path(self):
        """浏览希沃白板安装路径"""
        path = filedialog.askdirectory(title="选择希沃白板安装目录")
        if path:
            self.path_var.set(path)
            config_manager.set('paths.easinote_install_path', path)
            config_manager.save()
    
    def auto_detect_easinote(self):
        """自动检测希沃白板安装路径"""
        self.status_var.set("正在检测希沃白板安装路径...")
        
        def detect_thread():
            try:
                path = find_easinote_path()
                if path:
                    self.root.after(0, lambda: self.path_var.set(path))
                    config_manager.set('paths.easinote_install_path', path)
                    config_manager.save()
                    self.root.after(0, lambda: self.status_var.set(f"已找到希沃白板安装路径: {path}"))
                else:
                    self.root.after(0, lambda: messagebox.showerror("未找到", "无法自动检测希沃白板安装路径，请手动选择"))
                    self.root.after(0, lambda: self.status_var.set("就绪"))
            except Exception as e:
                logger.error(f"自动检测失败: {str(e)}")
                self.root.after(0, lambda: messagebox.showerror("错误", f"自动检测失败: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("就绪"))
        
        threading.Thread(target=detect_thread, daemon=True).start()
    
    def create_backup(self):
        """创建备份"""
        messagebox.showinfo("提示", "备份功能正在开发中")
    
    def apply_modifications(self):
        """应用修改"""
        messagebox.showinfo("提示", "修改功能正在开发中")
    
    def restore_original(self):
        """恢复原始文件"""
        messagebox.showinfo("提示", "恢复功能正在开发中")
    
    def save_settings(self):
        """保存设置"""
        try:
            config_manager.set('gui.theme', self.theme_var.get())
            # 保存窗口大小
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            config_manager.set('gui.window_size', [width, height])
            config_manager.save()
            messagebox.showinfo("成功", "设置已保存")
        except Exception as e:
            logger.error(f"保存设置失败: {str(e)}")
            messagebox.showerror("错误", f"保存设置失败: {str(e)}")

def start_gui():
    """启动图形界面"""
    logger.info("启动图形界面")
    
    root = tk.Tk()
    
    # 设置中文字体支持
    if sys.platform == 'win32':
        root.option_add('*Font', ('SimHei', 10))
    
    # 创建应用实例
    app = EasiNoteModifierGUI(root)
    
    # 主循环
    try:
        root.mainloop()
    except Exception as e:
        logger.error(f"GUI错误: {str(e)}", exc_info=True)
        raise