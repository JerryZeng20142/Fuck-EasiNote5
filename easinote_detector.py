import os
import winreg
from PySide6.QtCore import QObject, Signal, Slot

class EasiNoteDetector(QObject):
    """
    希沃白板安装路径检测器
    """
    # 信号定义
    detectionStarted = Signal()
    detectionFinished = Signal(str, bool)  # 参数：路径，是否成功
    pathSelected = Signal(str)  # 参数：选择的路径
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.install_path = ""
    
    @Slot()
    def detect_easinote_path(self):
        """
        自动检测希沃白板安装路径
        """
        self.detectionStarted.emit()
        
        path = ""
        success = False
        
        try:
            # 尝试从注册表获取安装路径
            path = self._get_path_from_registry()
            if path and os.path.exists(path):
                success = True
        except Exception as e:
            print(f"注册表读取错误: {e}")
        
        if not success:
            # 尝试常见的安装路径
            common_paths = [
                "C:\\Program Files (x86)\\Seewo\\EasiNote5",
                "C:\\Program Files\\Seewo\\EasiNote5",
                "D:\\Program Files (x86)\\Seewo\\EasiNote5",
                "D:\\Program Files\\Seewo\\EasiNote5"
            ]
            
            for p in common_paths:
                if os.path.exists(p):
                    path = p
                    success = True
                    break
        
        self.install_path = path
        self.detectionFinished.emit(path, success)
        
    @Slot(str)
    def selectPath(self, path):
        """
        手动选择路径
        """
        if os.path.exists(path):
            self.install_path = path
            self.pathSelected.emit(path)
    
    def _get_path_from_registry(self):
        """
        从注册表获取希沃白板安装路径
        """
        try:
            # 64位系统
            key_path = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\{22B9DE1A-C3C4-4C1E-8F93-0759C39A322F}"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ) as key:
                path, _ = winreg.QueryValueEx(key, "InstallLocation")
                return path
        except FileNotFoundError:
            try:
                # 32位系统
                key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{22B9DE1A-C3C4-4C1E-8F93-0759C39A322F}"
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ) as key:
                    path, _ = winreg.QueryValueEx(key, "InstallLocation")
                    return path
            except FileNotFoundError:
                return ""
        except Exception:
            return ""
