import QtQuick 2.15

// RinUI主题系统 - 定义Fluent Design风格的颜色和样式
QtObject {
    id: theme
    
    // 导出属性
    readonly property Theme light: Theme {}
    readonly property Theme dark: Theme {}
    
    // 定义主题颜色
    QtObject {
        id: Theme
        
        // 主色调
        readonly property color primary: "#0078d4"
        readonly property color primaryLight: "#106ebe"
        readonly property color primaryDark: "#005a9e"
        
        // 强调色
        readonly property color accent: "#e74c3c"
        readonly property color accentLight: "#d13438"
        readonly property color accentDark: "#b31919"
        
        // 背景色
        readonly property color background: "#f5f5f5"
        readonly property color surface: "#ffffff"
        readonly property color card: "#ffffff"
        
        // 文本色
        readonly property color text: "#333333"
        readonly property color textSecondary: "#666666"
        readonly property color textDisabled: "#999999"
        
        // 边框色
        readonly property color border: "#e0e0e0"
        readonly property color divider: "#e0e0e0"
        
        // 状态色
        readonly property color success: "#107c10"
        readonly property color warning: "#ffb900"
        readonly property color error: "#e74c3c"
        readonly property color info: "#0078d4"
        
        // 阴影
        readonly property real elevation: 2
        readonly property color shadow: "rgba(0, 0, 0, 0.1)"
        
        // 圆角
        readonly property real radius: 4
        readonly property real radiusLarge: 8
    }
    
    // 暗色主题覆盖
    Component.onCompleted: {
        dark.Theme.background = "#1a1a1a"
        dark.Theme.surface = "#252525"
        dark.Theme.card = "#333333"
        dark.Theme.text = "#ffffff"
        dark.Theme.textSecondary = "#cccccc"
        dark.Theme.textDisabled = "#999999"
        dark.Theme.border = "#404040"
        dark.Theme.divider = "#404040"
        dark.Theme.shadow = "rgba(0, 0, 0, 0.3)"
    }
}