import sys
import os
import logging
from PySide6.QtWidgets import QApplication, QMessageBox, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit
from PySide6.QtCore import Qt, Signal, QObject, QUrl, QAbstractTableModel, Slot, QDateTime
from PySide6.QtQml import QQmlApplicationEngine

# 配置日志记录
logger = logging.getLogger(__name__)

# 检查Rin-UI是否可用
RINUI_AVAILABLE = False
try:
    import RinUI
    RINUI_AVAILABLE = True
    logger.info("Rin-UI库可用")
except ImportError:
    logger.warning("Rin-UI库不可用")

# 导入我们的核心功能类
try:
    from audio_modifier import AudioModifier
    from config_manager import ConfigManager
    from log_manager import LogManager
    logger.info("成功导入核心功能类")
except ImportError as e:
    logger.error(f"导入核心功能类失败: {str(e)}")
    print(f"错误: 无法导入核心功能类: {str(e)}")

class GameFilesModel(QAbstractTableModel):
    """游戏文件列表模型，用于QML ListView显示"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = []
    
    def rowCount(self, parent=None):
        """返回行数"""
        return len(self._data)
    
    def columnCount(self, parent=None):
        """返回列数（文件名和路径）"""
        return 2
    
    def data(self, index, role=Qt.DisplayRole):
        """获取数据"""
        if not index.isValid():
            return None
        
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self._data[index.row()][index.column()]
        
        return None
    
    def setGameFiles(self, game_files):
        """设置游戏文件列表数据"""
        self.beginResetModel()
        self._data = game_files  # 格式: [(文件名, 文件路径), ...]
        self.endResetModel()
        logger.info(f"已更新游戏文件列表，共 {len(game_files)} 个文件")

class Backend(QObject):
    # 信号定义
    gameFilesUpdated = Signal(object)
    statusMessageChanged = Signal(str)
    logContentChanged = Signal(str)
    audioPathChanged = Signal(str)
    
    def __init__(self):
        super().__init__()
        logger.info("初始化后端服务...")
        self.config_manager = ConfigManager()
        self.audio_modifier = AudioModifier(self.config_manager)
        self.log_manager = LogManager()
        
        # 初始化游戏文件模型
        self.game_files_model = GameFilesModel()
        
        # 连接日志信号
        self.log_manager.log_updated.connect(self.update_log_content)
        
        # 状态变量
        self.selected_game_file = None
        self._selected_audio_path = ""
        self._status_message = "就绪"
        self._log_content = ""
        
        self.update_status("Rin-UI界面初始化完成")
        logger.info("后端服务初始化完成")
    
    # 属性定义，用于QML绑定
    @property
    def selectedAudioPath(self):
        return self._selected_audio_path
    
    @property
    def statusMessage(self):
        return self._status_message
    
    @property
    def logContent(self):
        return self._log_content
    
    def update_status(self, message):
        """更新状态消息"""
        self._status_message = f"[{QDateTime.currentDateTime().toString('HH:mm:ss')}] {message}"
        self.statusMessageChanged.emit(self._status_message)
        self.log_manager.log(self._status_message)
    
    def update_log_content(self, content):
        """更新日志内容"""
        self._log_content = content
        self.logContentChanged.emit(content)
    
    @Slot()
    def refreshGameFiles(self):
        """刷新游戏文件列表"""
        logger.info("刷新游戏文件列表...")
        self.update_status("正在刷新游戏文件列表...")
        try:
            game_files = self.audio_modifier.list_games()
            # 将游戏文件数据设置到模型中
            self.game_files_model.setGameFiles(game_files)
            # 发射信号通知QML数据已更新
            self.gameFilesUpdated.emit(self.game_files_model)
            
            if not game_files:
                self.update_status("未找到游戏目录，请检查配置")
            else:
                self.update_status(f"已找到 {len(game_files)} 个游戏文件")
        except Exception as e:
            error_msg = f"刷新游戏文件列表时出错: {str(e)}"
            self.update_status(error_msg)
            logger.error(error_msg)
    
    @Slot(str)
    def selectGameFile(self, file_path):
        """选择游戏文件"""
        logger.info(f"选择游戏文件: {file_path}")
        self.selected_game_file = file_path
        self.update_status(f"已选择游戏文件: {os.path.basename(file_path)}")
    
    @Slot()
    def browseAudioFile(self):
        """浏览音频文件"""
        logger.info("浏览音频文件")
        # 在实际应用中，这个方法应该通过QML的文件对话框来实现
        # 这里我们通过PySide6的对话框作为备选
        from PySide6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            None, "选择音频文件", "", "音频文件 (*.wav *.mp3 *.ogg *.flac)"
        )
        
        if file_path:
            self._selected_audio_path = file_path
            self.audioPathChanged.emit(file_path)
            self.update_status(f"已选择音频文件: {os.path.basename(file_path)}")
    
    @Slot()
    def previewAudio(self):
        """预览音频"""
        logger.info(f"预览音频: {self._selected_audio_path}")
        if not self._selected_audio_path:
            self.update_status("请先选择音频文件")
            return
        
        try:
            self.update_status("正在预览音频...")
            # 检查是否安装了pygame来进行音频预览
            try:
                import pygame
                pygame.mixer.init()
                pygame.mixer.music.load(self._selected_audio_path)
                pygame.mixer.music.play()
                self.update_status("正在播放预览音频")
            except ImportError:
                self.update_status("未安装pygame，无法预览音频")
        except Exception as e:
            error_msg = f"预览音频时出错: {str(e)}"
            self.update_status(error_msg)
            logger.error(error_msg)
    
    @Slot()
    def modifyBgm(self):
        """修改背景音乐"""
        logger.info(f"修改背景音乐: {self.selected_game_file} -> {self._selected_audio_path}")
        if not self.selected_game_file:
            self.update_status("请先选择游戏文件")
            return
        
        if not self._selected_audio_path:
            self.update_status("请先选择音频文件")
            return
        
        try:
            self.update_status("正在修改背景音乐...")
            success = self.audio_modifier.replace_bgm(self.selected_game_file, self._selected_audio_path)
            if success:
                self.update_status(f"成功修改 {os.path.basename(self.selected_game_file)} 的背景音乐")
            else:
                self.update_status("修改背景音乐失败")
        except Exception as e:
            error_msg = f"修改背景音乐时出错: {str(e)}"
            self.update_status(error_msg)
            logger.error(error_msg)
    
    @Slot()
    def restoreBgm(self):
        """恢复默认背景音乐"""
        logger.info(f"恢复默认背景音乐: {self.selected_game_file}")
        if not self.selected_game_file:
            self.update_status("请先选择游戏文件")
            return
        
        try:
            self.update_status("正在恢复默认背景音乐...")
            success = self.audio_modifier.restore_default_bgm(self.selected_game_file)
            if success:
                self.update_status(f"成功恢复 {os.path.basename(self.selected_game_file)} 的默认背景音乐")
            else:
                self.update_status("恢复默认背景音乐失败")
        except Exception as e:
            error_msg = f"恢复默认背景音乐时出错: {str(e)}"
            self.update_status(error_msg)
            logger.error(error_msg)
    
    @Slot()
    def showConfigDialog(self):
        """显示配置对话框"""
        logger.info("显示配置对话框")
        current_path = self.config_manager.get_config("easinote_path", "")
        # 使用PySide6的对话框选择目录
        from PySide6.QtWidgets import QFileDialog
        new_path = QFileDialog.getExistingDirectory(
            None, "选择希沃白板5安装目录", current_path
        )
        
        if new_path:
            self.config_manager.set_config("easinote_path", new_path)
            self.config_manager.save_config()
            self.update_status(f"已更新希沃白板5路径: {new_path}")
            # 重新加载游戏文件
            self.refreshGameFiles()
    
    @Slot(str)
    def showFileInfo(self, file_path):
        """显示文件信息"""
        logger.info(f"显示文件信息: {file_path}")
        try:
            # 获取文件信息
            file_stats = os.stat(file_path)
            file_name = os.path.basename(file_path)
            file_size = file_stats.st_size / 1024  # KB
            import datetime
            file_time = datetime.datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            info_text = f"文件名: {file_name}\n"
            info_text += f"文件大小: {file_size:.2f} KB\n"
            info_text += f"修改时间: {file_time}\n"
            
            QMessageBox.information(None, "文件信息", info_text)
        except Exception as e:
            error_msg = f"获取文件信息时出错: {str(e)}"
            self.update_status(error_msg)
            logger.error(error_msg)

# 定义槽函数，用于从QML调用Python方法
@Slot(str)
def set_audio_path_from_qml(backend, file_path):
    """从QML设置音频路径"""
    logger.info(f"从QML设置音频路径: {file_path}")
    backend._selected_audio_path = file_path
    backend.audioPathChanged.emit(file_path)
    backend.update_status(f"已选择音频文件: {os.path.basename(file_path)}")

@Slot(result=str)
def get_easinote_path(backend):
    """获取希沃白板5路径"""
    return backend.config_manager.get_config("easinote_path", "")

@Slot(str)
def set_easinote_path(backend, path):
    """设置希沃白板5路径"""
    logger.info(f"设置希沃白板5路径: {path}")
    backend.config_manager.set_config("easinote_path", path)
    backend.config_manager.save_config()
    backend.update_status(f"已更新希沃白板5路径: {path}")

def run_rin_ui():
    """运行Rin-UI界面"""
    logger.info("启动Rin-UI界面...")
    
    # 创建QApplication
    app = QApplication(sys.argv) if QApplication.instance() is None else QApplication.instance()
    app.setApplicationName("希沃白板5修改工具")
    app.setOrganizationName("某中学生叫姐姐Jerry")
    
    # 尝试加载Rin-UI库
    try:
        # 导入Rin-UI模块并注册组件
        from RinUI import registerTypes
        registerTypes()
        logger.info("成功加载Rin-UI库并注册组件")
    except ImportError as e:
        logger.warning(f"无法加载Rin-UI，将尝试使用PySide6的默认样式: {e}")
        # 使用Fusion样式作为备选
        app.setStyle("Fusion")
    
    # 创建后端对象
    backend = Backend()
    
    # 创建QQmlApplicationEngine
    engine = QQmlApplicationEngine()
    
    # 获取上下文
    context = engine.rootContext()
    
    # 将后端对象暴露给QML
    context.setContextProperty("backend", backend)
    
    # 注册自定义槽函数
    context.setContextProperty("setAudioPathFromQml", lambda path: set_audio_path_from_qml(backend, path))
    context.setContextProperty("getEasinotePath", lambda: get_easinote_path(backend))
    context.setContextProperty("setEasinotePath", lambda path: set_easinote_path(backend, path))
    
    # 加载QML文件
    qml_file = os.path.join(os.path.dirname(__file__), "ui", "main.qml")
    
    if os.path.exists(qml_file):
        # 检查文件是否为UTF-8编码
        try:
            with open(qml_file, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info("QML文件编码检查通过")
        except UnicodeDecodeError:
            logger.warning("QML文件可能不是UTF-8编码，尝试加载")
        
        # 加载QML文件
        engine.load(QUrl.fromLocalFile(qml_file))
        
        # 检查是否成功加载QML
        if not engine.rootObjects():
            error_msg = "无法加载QML界面，根对象为空"
            logger.error(error_msg)
            QMessageBox.critical(None, "错误", f"无法加载QML界面，请检查文件格式是否正确。")
            return 1
        
        # 连接游戏文件更新信号
        backend.gameFilesUpdated.connect(lambda model: logger.info(f"游戏文件已更新，共{model.rowCount()}个文件"))
        
        # 初始刷新游戏文件列表
        backend.refreshGameFiles()
        
        # 启动事件循环
        logger.info("Rin-UI界面启动成功")
        return app.exec()
    else:
        # 如果QML文件不存在，创建回退UI
        error_msg = f"QML文件不存在: {qml_file}"
        logger.error(error_msg)
        QMessageBox.warning(None, "警告", f"无法找到界面文件: {qml_file}\n将使用回退界面。")
        return create_fallback_ui(app, backend)

def create_fallback_ui(app, backend):
    """创建简单的回退UI界面"""
    logger.info("创建回退UI界面")
    
    # 创建主窗口
    main_window = QWidget()
    main_window.setWindowTitle("希沃白板5修改工具 (回退界面)")
    main_window.resize(800, 600)
    
    # 创建主布局
    main_layout = QVBoxLayout(main_window)
    main_layout.setSpacing(10)
    main_layout.setContentsMargins(10, 10, 10, 10)
    
    # 添加提示标签
    label = QLabel("无法加载Rin-UI界面，已启用回退界面。请确保ui/main.qml文件存在且格式正确。")
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("color: #d32f2f; font-weight: bold;")
    main_layout.addWidget(label)
    
    # 添加操作按钮
    button_layout = QVBoxLayout()
    
    refresh_button = QPushButton("刷新游戏文件列表")
    refresh_button.clicked.connect(backend.refreshGameFiles)
    button_layout.addWidget(refresh_button)
    
    browse_button = QPushButton("浏览音频文件")
    browse_button.clicked.connect(backend.browseAudioFile)
    button_layout.addWidget(browse_button)
    
    modify_button = QPushButton("修改背景音乐")
    modify_button.clicked.connect(backend.modifyBgm)
    button_layout.addWidget(modify_button)
    
    restore_button = QPushButton("恢复默认背景音乐")
    restore_button.clicked.connect(backend.restoreBgm)
    button_layout.addWidget(restore_button)
    
    config_button = QPushButton("设置希沃白板路径")
    config_button.clicked.connect(backend.showConfigDialog)
    button_layout.addWidget(config_button)
    
    main_layout.addLayout(button_layout)
    
    # 添加日志文本区域
    log_label = QLabel("操作日志:")
    log_label.setStyleSheet("font-weight: bold;")
    main_layout.addWidget(log_label)
    
    log_text = QTextEdit()
    log_text.setReadOnly(True)
    log_text.setLineWrapMode(QTextEdit.WidgetWidth)
    log_text.setStyleSheet("font-family: Consolas, Monaco, 'Courier New'; font-size: 10pt;")
    main_layout.addWidget(log_text, 1)
    
    # 连接后端的日志信号到文本区域
    backend.logContentChanged.connect(log_text.setPlainText)
    
    # 显示窗口
    main_window.show()
    
    # 添加初始日志
    backend.update_status("回退界面已启动")
    backend.update_status("请检查ui目录下是否存在main.qml文件")
    
    # 运行应用程序
    return app.exec()

# 备选UI实现 - 当Rin-UI不可用时的PySide6原生实现
class EasiNote5ToolPySide6(QApplication):
    """基于PySide6的备选界面实现"""
    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName("希沃白板5修改工具 (备选界面)")
        self.setStyle("Fusion")
        
    def run(self):
        """运行备选界面"""
        logger.info("启动PySide6备选界面")
        # 这里可以实现一个简单的PySide6界面作为备选
        QMessageBox.information(None, "信息", "Rin-UI不可用，使用备选界面")
        # 可以在这里添加简单的备选界面实现
        return 0

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sys.exit(run_rin_ui())