# Fuck-EasiNote5

希沃白板5修改工具，支持各种自定义设置和功能增强。

## 安装依赖

```bash
pip install -r requirements.txt

# 或者使用Test PyPI安装RinUI（如果官方PyPI尚未发布）
pip install PySide6 darkdetect
pip install -i https://test.pypi.org/simple/ RinUI --no-deps
```

## 使用方法

直接运行主程序：

```bash
python main.py
```

## 关于RinUI

本项目使用RinUI作为UI框架，RinUI是一个类Fluent Design的Qt Quick (QML) UI库。

### RinUI配置

1. 确保已安装必要的依赖：PySide6, darkdetect, RinUI
2. 程序会自动尝试加载RinUI，如果失败将回退到传统Tkinter界面
3. RinUI相关文件存放在`ui/RinUI`目录中

## 运行环境

- Python 3.6 或更高版本
- 主要依赖：PySide6, RinUI, darkdetect

## 开发状态

- [x] 图形界面框架（RinUI）
- [ ] 备份功能
- [ ] 修改功能
- [ ] 恢复功能
- [ ] 完整的功能实现

## 注意事项

- 功能实现正在开发中，所有功能按钮目前显示"开发中"提示
- 建议以管理员权限运行程序以确保所有功能正常工作
- 使用此工具风险自负，请确保备份原始文件
- 这是一个希沃白板5修改工具的简化版本，目前仅包含图形界面框架
- 此工具目前仅为界面演示版本，所有功能按钮仅显示提示信息
- 完整功能将在后续版本中逐步实现

## 许可证

本项目仅供学习和研究使用。