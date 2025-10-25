import QtQuick 2.15
import QtQuick.Controls 2.15

// 文本框组件 - Fluent Design风格的输入框
TextField {
    id: control
    
    // 自定义属性
    property bool outlined: false
    
    // 基本尺寸
    implicitWidth: 200
    implicitHeight: 36
    
    // 背景样式
    background: Rectangle {
        id: background
        border.width: control.outlined ? 1 : (control.hovered || control.focused) ? 2 : 0
        border.color: control.focused ? "#0078d4" : control.hovered ? "#0078d4" : "#e0e0e0"
        radius: 4
        color: control.outlined ? "transparent" : control.background
        
        // 聚焦时的动画效果
        Behavior on border.color {
            ColorAnimation { duration: 200 }
        }
    }
    
    // 文本样式
    contentItem: TextInput {
        id: contentItem
        text: control.text
        font.pointSize: 14
        font.family: "Microsoft YaHei"
        color: control.enabled ? (control.error ? "#e74c3c" : "#333") : "#999"
        selectionColor: "#0078d4"
        selectedTextColor: "white"
        horizontalAlignment: TextInput.AlignLeft
        verticalAlignment: TextInput.AlignVCenter
        
        // 确保文本在边框内有适当的边距
        leftPadding: 10
        rightPadding: 10
        topPadding: 0
        bottomPadding: 0
    }
    
    // 占位符样式
    placeholderTextColor: "#999999"
    
    // 鼠标区域设置
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onClicked: control.focus = true
    }
}