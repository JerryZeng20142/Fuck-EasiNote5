#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图形用户界面模块
提供希沃白板5修改工具的可视化操作界面
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from audio_modifier import AudioModifier
from config import Config
from utils import logger, get_file_list, get_file_info

class EasiNoteToolGUI:
    """
    希沃白板5修改工具的图形用户界面类
    """
    
    def __init__(self, root):
        """
        初始化GUI界面
        
        Args:
            root: Tkinter根窗口
        """
        self.root = root
        self.root.title("希沃白板5修改工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 加载配置
        self.config = Config()
        # 初始化音频修改器
        self.modifier = AudioModifier(self.config)
        
        # 设置中文字体支持
        self._setup_fonts()
        
        # 创建UI组件
        self._create_widgets()
        
        # 加载游戏文件列表
        self._load_game_files()
        
        logger.info("GUI界面初始化完成")
    
    def _setup_fonts(self):
        """
        设置字体配置，确保中文显示正常
        """
        # 在Windows上，Tkinter通常可以很好地支持中文字体
        # 这里设置默认字体，也可以根据需要自定义
        self.default_font = ('SimHei', 10)
        self.header_font = ('SimHei', 12, 'bold')
    
    def _create_widgets(self):
        """
        创建UI组件
        """
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题区域
        self._create_header(main_frame)
        
        # 创建游戏文件列表区域
        self._create_game_list_section(main_frame)
        
        # 创建音频文件选择区域
        self._create_audio_selection_section(main_frame)
        
        # 创建操作按钮区域
        self._create_buttons_section(main_frame)
        
        # 创建日志/消息区域
        self._create_log_section(main_frame)
        
        # 创建状态栏
        self._create_status_bar()
    
    def _create_header(self, parent):
        """
        创建标题区域
        """
        header_frame = ttk.Frame(parent, padding="5")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(
            header_frame, 
            text="希沃白板5修改工具", 
            font=self.header_font
        )
        title_label.pack(side=tk.LEFT)
        
        version_label = ttk.Label(
            header_frame, 
            text="版本: 0.1.0", 
            font=self.default_font
        )
        version_label.pack(side=tk.RIGHT)
        
        author_label = ttk.Label(
            header_frame, 
            text="作者: 某中学生叫姐姐Jerry", 
            font=self.default_font
        )
        author_label.pack(side=tk.RIGHT, padx=(0, 20))
    
    def _create_game_list_section(self, parent):
        """
        创建游戏文件列表区域
        """
        section_frame = ttk.LabelFrame(parent, text="小游戏文件列表", padding="5")
        section_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 创建工具栏
        toolbar_frame = ttk.Frame(section_frame, padding="5")
        toolbar_frame.pack(fill=tk.X, pady=(0, 5))
        
        # 刷新按钮
        refresh_button = ttk.Button(
            toolbar_frame, 
            text="刷新列表", 
            command=self._load_game_files
        )
        refresh_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 配置按钮
        config_button = ttk.Button(
            toolbar_frame, 
            text="配置路径", 
            command=self._show_config_dialog
        )
        config_button.pack(side=tk.LEFT)
        
        # 创建列表
        list_frame = ttk.Frame(section_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 列表框
        self.game_listbox = tk.Listbox(
            list_frame, 
            yscrollcommand=scrollbar.set,
            font=self.default_font,
            selectmode=tk.SINGLE
        )
        self.game_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.game_listbox.yview)
        
        # 绑定双击事件
        self.game_listbox.bind('<Double-1>', self._on_game_double_click)
    
    def _create_audio_selection_section(self, parent):
        """
        创建音频文件选择区域
        """
        section_frame = ttk.LabelFrame(parent, text="音频文件选择", padding="5")
        section_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 音频文件路径显示
        path_frame = ttk.Frame(section_frame, padding="5")
        path_frame.pack(fill=tk.X)
        
        self.audio_path_var = tk.StringVar()
        audio_entry = ttk.Entry(
            path_frame, 
            textvariable=self.audio_path_var,
            width=60,
            font=self.default_font
        )
        audio_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # 浏览按钮
        browse_button = ttk.Button(
            path_frame, 
            text="浏览...", 
            command=self._browse_audio_file
        )
        browse_button.pack(side=tk.RIGHT)
    
    def _create_buttons_section(self, parent):
        """
        创建操作按钮区域
        """
        section_frame = ttk.Frame(parent, padding="5")
        section_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 修改背景音乐按钮
        modify_button = ttk.Button(
            section_frame, 
            text="修改背景音乐", 
            command=self._modify_bgm,
            width=20
        )
        modify_button.pack(side=tk.LEFT, padx=5)
        
        # 恢复默认按钮
        restore_button = ttk.Button(
            section_frame, 
            text="恢复默认背景音乐", 
            command=self._restore_bgm,
            width=20
        )
        restore_button.pack(side=tk.LEFT, padx=5)
        
        # 预览按钮
        preview_button = ttk.Button(
            section_frame, 
            text="预览音频", 
            command=self._preview_audio,
            width=15
        )
        preview_button.pack(side=tk.LEFT, padx=5)
    
    def _create_log_section(self, parent):
        """
        创建日志/消息区域
        """
        section_frame = ttk.LabelFrame(parent, text="操作日志", padding="5")
        section_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 滚动条
        scrollbar = ttk.Scrollbar(section_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 文本框
        self.log_text = tk.Text(
            section_frame, 
            yscrollcommand=scrollbar.set,
            font=self.default_font,
            wrap=tk.WORD,
            height=10
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # 设置为只读
        self.log_text.config(state=tk.DISABLED)
    
    def _create_status_bar(self):
        """
        创建状态栏
        """
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        
        status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=self.default_font
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _load_game_files(self):
        """
        加载游戏文件列表
        """
        try:
            self.status_var.set("正在加载游戏文件...")
            self.game_listbox.delete(0, tk.END)
            
            games_dir = self.config.get_games_directory()
            
            if not os.path.exists(games_dir):
                self._add_log(f"错误: 未找到游戏目录: {games_dir}")
                self._add_log("请检查配置中的希沃白板5安装路径是否正确")
                self.status_var.set("就绪")
                return
            
            # 获取游戏文件列表（假设为zip或xexb格式）
            game_files = get_file_list(games_dir, ['.zip', '.xexb'])
            
            if not game_files:
                self._add_log(f"未在目录中找到游戏文件: {games_dir}")
            else:
                self._add_log(f"找到 {len(game_files)} 个游戏文件")
                for game_file in game_files:
                    # 只显示文件名，不显示完整路径
                    file_name = os.path.basename(game_file)
                    self.game_listbox.insert(tk.END, file_name)
                    # 将完整路径存储在列表项的字典中
                    self.game_listbox.file_path = getattr(self.game_listbox, 'file_path', {})
                    self.game_listbox.file_path[file_name] = game_file
                    
        except Exception as e:
            self._add_log(f"加载游戏文件时出错: {str(e)}")
        finally:
            self.status_var.set("就绪")
    
    def _browse_audio_file(self):
        """
        浏览选择音频文件
        """
        file_types = [
            ("音频文件", "*.mp3 *.wav *.ogg"),
            ("MP3文件", "*.mp3"),
            ("WAV文件", "*.wav"),
            ("OGG文件", "*.ogg"),
            ("所有文件", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="选择音频文件",
            filetypes=file_types
        )
        
        if file_path:
            self.audio_path_var.set(file_path)
            file_info = get_file_info(file_path)
            if file_info:
                self._add_log(f"已选择音频文件: {file_info['name']} ({file_info['size_mb']} MB)")
    
    def _modify_bgm(self):
        """
        修改背景音乐
        """
        # 获取选中的游戏文件
        selected_indices = self.game_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("警告", "请先选择一个游戏文件")
            return
        
        selected_file = self.game_listbox.get(selected_indices[0])
        game_file_path = self.game_listbox.file_path.get(selected_file)
        
        # 获取音频文件路径
        audio_file = self.audio_path_var.get()
        if not audio_file or not os.path.exists(audio_file):
            messagebox.showwarning("警告", "请先选择一个有效的音频文件")
            return
        
        # 确认操作
        if not messagebox.askyesno("确认", f"确定要修改 {selected_file} 的背景音乐吗？\n修改前会自动备份原文件"):
            return
        
        # 在后台线程中执行修改操作
        self.status_var.set("正在修改背景音乐...")
        thread = threading.Thread(
            target=self._modify_bgm_thread, 
            args=(game_file_path, audio_file)
        )
        thread.daemon = True
        thread.start()
    
    def _modify_bgm_thread(self, game_file_path, audio_file):
        """
        在后台线程中执行背景音乐修改
        """
        try:
            self._add_log(f"开始修改游戏文件: {os.path.basename(game_file_path)}")
            success = self.modifier.modify_bgm(game_file_path, audio_file)
            
            if success:
                self._add_log("背景音乐修改成功！")
                self.root.after(0, lambda: messagebox.showinfo("成功", "背景音乐修改成功！"))
            else:
                self._add_log("背景音乐修改失败！")
                self.root.after(0, lambda: messagebox.showerror("失败", "背景音乐修改失败，请查看日志获取详细信息"))
                
        except Exception as e:
            self._add_log(f"修改背景音乐时出错: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("错误", f"修改过程中发生错误: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.status_var.set("就绪"))
    
    def _restore_bgm(self):
        """
        恢复默认背景音乐
        """
        # 获取选中的游戏文件
        selected_indices = self.game_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("警告", "请先选择一个游戏文件")
            return
        
        selected_file = self.game_listbox.get(selected_indices[0])
        game_file_path = self.game_listbox.file_path.get(selected_file)
        
        # 确认操作
        if not messagebox.askyesno("确认", f"确定要恢复 {selected_file} 的默认背景音乐吗？"):
            return
        
        # 在后台线程中执行恢复操作
        self.status_var.set("正在恢复默认背景音乐...")
        thread = threading.Thread(
            target=self._restore_bgm_thread, 
            args=(game_file_path,)
        )
        thread.daemon = True
        thread.start()
    
    def _restore_bgm_thread(self, game_file_path):
        """
        在后台线程中执行背景音乐恢复
        """
        try:
            self._add_log(f"开始恢复游戏文件: {os.path.basename(game_file_path)}")
            success = self.modifier.restore_bgm(game_file_path)
            
            if success:
                self._add_log("背景音乐恢复成功！")
                self.root.after(0, lambda: messagebox.showinfo("成功", "背景音乐恢复成功！"))
            else:
                self._add_log("背景音乐恢复失败！")
                self.root.after(0, lambda: messagebox.showerror("失败", "背景音乐恢复失败，请查看日志获取详细信息"))
                
        except Exception as e:
            self._add_log(f"恢复背景音乐时出错: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("错误", f"恢复过程中发生错误: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.status_var.set("就绪"))
    
    def _preview_audio(self):
        """
        预览音频文件
        注：此功能需要pygame库支持
        """
        audio_file = self.audio_path_var.get()
        if not audio_file or not os.path.exists(audio_file):
            messagebox.showwarning("警告", "请先选择一个有效的音频文件")
            return
        
        try:
            # 尝试导入pygame
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            self._add_log(f"正在播放音频: {os.path.basename(audio_file)}")
            
            # 显示播放提示
            def stop_playing():
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                    self._add_log("音频播放已停止")
            
            play_window = tk.Toplevel(self.root)
            play_window.title("音频预览")
            play_window.geometry("300x100")
            play_window.resizable(False, False)
            
            ttk.Label(play_window, text=f"正在播放: {os.path.basename(audio_file)}").pack(pady=20)
            
            button_frame = ttk.Frame(play_window)
            button_frame.pack(pady=10)
            
            ttk.Button(button_frame, text="停止播放", command=lambda: [stop_playing(), play_window.destroy()]).pack()
            
        except ImportError:
            messagebox.showinfo("提示", "音频预览功能需要安装pygame库\n请运行: pip install pygame")
        except Exception as e:
            self._add_log(f"音频预览时出错: {str(e)}")
            messagebox.showerror("错误", f"音频预览失败: {str(e)}")
    
    def _show_config_dialog(self):
        """
        显示配置对话框
        """
        dialog = tk.Toplevel(self.root)
        dialog.title("配置")
        dialog.geometry("500x200")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 创建配置项
        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 希沃白板5路径
        ttk.Label(frame, text="希沃白板5安装路径:", font=self.default_font).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        path_var = tk.StringVar(value=self.config.get('easinote_path'))
        path_entry = ttk.Entry(frame, textvariable=path_var, width=40, font=self.default_font)
        path_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        def browse_path():
            path = filedialog.askdirectory(title="选择希沃白板5安装目录")
            if path:
                path_var.set(path)
        
        ttk.Button(frame, text="浏览...", command=browse_path).grid(row=0, column=2, sticky=tk.W, pady=5, padx=5)
        
        # 按钮区域
        button_frame = ttk.Frame(dialog, padding="10")
        button_frame.pack(fill=tk.X)
        
        def save_config():
            self.config.set('easinote_path', path_var.get())
            self.config.save_config()
            dialog.destroy()
            # 重新加载游戏文件列表
            self._load_game_files()
            self._add_log("配置已保存并重新加载游戏文件列表")
        
        ttk.Button(button_frame, text="保存", command=save_config).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _on_game_double_click(self, event):
        """
        游戏文件双击事件处理
        """
        selected_indices = self.game_listbox.curselection()
        if selected_indices:
            selected_file = self.game_listbox.get(selected_indices[0])
            game_file_path = self.game_listbox.file_path.get(selected_file)
            file_info = get_file_info(game_file_path)
            
            if file_info:
                messagebox.showinfo(
                    "文件信息",
                    f"文件名: {file_info['name']}\n" +
                    f"路径: {file_info['path']}\n" +
                    f"大小: {file_info['size_mb']} MB\n" +
                    f"修改时间: {file_info['modified']}"
                )
    
    def _add_log(self, message):
        """
        添加日志消息
        """
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)  # 自动滚动到末尾
        self.log_text.config(state=tk.DISABLED)
        
        # 同时记录到日志文件
        logger.info(message)

def run_gui():
    """
    运行GUI界面
    """
    root = tk.Tk()
    # 设置中文字体
    root.option_add("*Font", ("SimHei", 10))
    app = EasiNoteToolGUI(root)
    root.mainloop()