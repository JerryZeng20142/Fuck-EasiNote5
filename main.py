import sys
from RinUI import RinUIWindow
from RinUI.core.config import Theme
from PySide6.QtWidgets import QApplication, QFileDialog
from PySide6.QtCore import QUrl, QObject, Slot, Signal, QTimer
from PySide6.QtGui import QGuiApplication
from easinote_detector import EasiNoteDetector
from config_manager import ConfigManager

class ThemeManager(QObject):
    """
    主题管理器，用于管理应用程序的主题设置
    """
    
    # 主题变化信号
    themeChanged = Signal(str)
    
    def __init__(self, config_manager, window):
        super().__init__()
        self.config_manager = config_manager
        self.window = window
        self.current_theme = None
        
        # 加载初始主题
        self.load_theme()
    
    def load_theme(self):
        """
        从配置中加载主题
        """
        self.current_theme = self.config_manager.get_theme()
        
        # 应用主题
        self.apply_theme(self.current_theme)
    
    def apply_theme(self, theme):
        """
        应用主题
        
        参数：
            theme: 主题名称（"auto", "dark" 或 "light"）
        """
        if theme == "auto":
            # 使用RinUI的自动主题功能
            self.window.setTheme(Theme.Auto)
        elif theme == "dark":
            self.window.setTheme(Theme.Dark)
        elif theme == "light":
            self.window.setTheme(Theme.Light)
    
    @Slot(result=str)
    def getCurrentTheme(self):
        """
        获取当前主题
        
        返回：
            str: 当前主题（"auto", "dark" 或 "light"）
        """
        return self.current_theme
    
    @Slot(str)
    def setTheme(self, theme):
        """
        设置主题
        
        参数：
            theme: 主题名称（"auto", "dark" 或 "light"）
        """
        # 保存主题设置
        self.config_manager.set_theme(theme)
        self.current_theme = theme
        
        # 应用主题
        self.apply_theme(theme)
        
        # 发送主题变化信号
        self.themeChanged.emit(theme)

class FileDialogManager(QObject):
    """
    文件对话框管理器，用于处理文件和文件夹选择
    """
    
    # 路径选择完成信号
    pathSelected = Signal(str)
    
    def __init__(self):
        super().__init__()
    
    @Slot(result=str)
    def selectFolder(self):
        """
        选择文件夹
        
        返回：
            str: 选择的文件夹路径
        """
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        dialog.setWindowTitle("选择希沃白板5安装目录")
        dialog.setDirectory("C:/Program Files (x86)/Seewo")
        
        if dialog.exec() == QFileDialog.Accepted:
            selected_files = dialog.selectedFiles()
            if selected_files:
                return selected_files[0]
        return ""

if __name__ == '__main__':
    # 创建应用程序实例
    app = QApplication(sys.argv)
    
    # 创建配置管理器
    config_manager = ConfigManager()
    
    # 创建希沃白板检测器
    detector = EasiNoteDetector()
    
    # 创建文件对话框管理器
    file_dialog_manager = FileDialogManager()
    
    # 创建RinUI窗口，加载QML文件
    import os
    app_dir = os.path.dirname(os.path.abspath(__file__))
    ui_dir = os.path.join(app_dir, "ui")
    main_qml_path = os.path.join(ui_dir, "main.qml")
    window = RinUIWindow(main_qml_path)
    
    # 添加QML导入路径，指向应用的根目录和ui目录
    window.engine.addImportPath(app_dir)
    window.engine.addImportPath(ui_dir)
    window.engine.addImportPath(".")
    window.engine.addImportPath("ui")
    
    # 创建主题管理器
    theme_manager = ThemeManager(config_manager, window)
    
    # 将检测器暴露给QML
    window.engine.rootContext().setContextProperty("EasiNoteDetector", detector)
    
    # 将主题管理器暴露给QML
    window.engine.rootContext().setContextProperty("ThemeManager", theme_manager)
    
    # 将文件对话框管理器暴露给QML
    window.engine.rootContext().setContextProperty("FileDialogManager", file_dialog_manager)
    
    # 显示窗口
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())
