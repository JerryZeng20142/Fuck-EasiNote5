# RinUI集成示例

这是一个使用RinUI UI库构建的示例项目，展示了如何将RinUI集成到Python + PySide6项目中。

## 技术栈

- Python 3.8+
- PySide6
- RinUI (Fluent Design风格的QML UI库)

## 功能特点

- 现代化的Fluent Design风格界面
- 支持深色/浅色主题切换
- 响应式设计
- 丰富的UI组件库

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行项目

```bash
python main.py
```

## 项目结构

```
├── ui/
│   └── main.qml          # 主界面QML文件
├── main.py               # 项目入口文件
├── requirements.txt      # 项目依赖
├── .gitignore           # Git忽略配置
└── README.md            # 项目说明文档
```

## 使用RinUI组件

在QML文件中，你可以直接使用RinUI提供的组件：

```qml
import RinUI 1.0

FluentWindow {
    // 窗口配置
    
    Button {
        text: "点击我"
        onClicked: {
            console.log("按钮被点击了！")
        }
    }
    
    CheckBox {
        text: "启用功能"
        checked: true
    }
    
    Switch {
        text: "主题切换"
        onCheckedChanged: {
            ThemeManager.toggle_theme(checked ? "Dark" : "Light")
        }
    }
}
```

## 主题设置

你可以在Python代码中设置初始主题：

```python
from RinUI.core.config import Theme

# 设置深色主题
window.setTheme(Theme.Dark)

# 设置浅色主题
window.setTheme(Theme.Light)

# 自动跟随系统主题
window.setTheme(Theme.Auto)
```

## 注意事项

1. 确保使用最新版本的RinUI
2. 部分高级功能可能只在Windows 11上可用
3. 主题切换需要ThemeManager对象

## 许可证

MIT License
