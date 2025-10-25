import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

// RinUI控件库 - 类Fluent Design风格控件

// 按钮组件 - 支持Fluent风格的按钮样式
Button {
    id: control
    
    // 自定义属性
    property bool primary: false
    property bool accent: false
    
    // 样式设置
    background: Rectangle {
        implicitWidth: 100
        implicitHeight: 36
        radius: 4
        
        // 根据状态和属性设置背景色
        color: control.pressed ? 
               (control.primary ? "#005a9e" : control.accent ? "#b31919" : "#d0d0d0") :
               (control.hovered ? 
                (control.primary ? "#106ebe" : control.accent ? "#d13438" : "#e0e0e0") :
                (control.primary ? "#0078d4" : control.accent ? "#e74c3c" : "#f0f0f0"))
        
        // 边框
        border.color: control.focused ? 
                      (control.primary ? "#0078d4" : "#0078d4") : 
                      "transparent"
        border.width: control.focused ? 2 : 0
    }
    
    // 文本样式
    contentItem: Text {
        text: control.text
        font.pointSize: 14
        font.family: "Microsoft YaHei"
        color: control.primary || control.accent ? "white" : "#333"
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
    
    // 鼠标区域设置
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
    }
}