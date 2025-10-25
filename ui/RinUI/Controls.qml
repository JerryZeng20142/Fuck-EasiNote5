import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "../RinUI" // 导入主题

// RinUI控件库 - 类Fluent Design风格控件

// 按钮组件 - 支持Fluent风格的按钮样式
Button {
    id: control
    
    // 自定义属性
    property bool primary: false
    property bool accent: false
    property bool darkMode: false
    
    // 使用主题颜色
    property var currentTheme: darkMode ? Theme {}.dark.Theme : Theme {}.light.Theme
    
    // 样式设置
    background: Rectangle {
        implicitWidth: 100
        implicitHeight: 36
        radius: currentTheme.radius
        
        // 根据状态和属性设置背景色
        color: control.pressed ? 
               (control.primary ? currentTheme.primaryDark : control.accent ? currentTheme.accentDark : "#d0d0d0") :
               (control.hovered ? 
                (control.primary ? currentTheme.primaryLight : control.accent ? currentTheme.accentLight : "#e0e0e0") :
                (control.primary ? currentTheme.primary : control.accent ? currentTheme.accent : "#f0f0f0"))
        
        // 边框
        border.color: control.focused ? 
                      (control.primary ? currentTheme.primary : currentTheme.primary) : 
                      "transparent"
        border.width: control.focused ? 2 : 0
    }
    
    // 文本样式
    contentItem: Text {
        text: control.text
        font.pointSize: 14
        font.family: "Microsoft YaHei"
        color: control.primary || control.accent ? "white" : currentTheme.text
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
    
    // 鼠标区域设置
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
    }
}