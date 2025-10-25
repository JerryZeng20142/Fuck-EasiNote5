import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.impl 2.15
import QtQuick.PrivateWidgets 2.15

// 下拉选择框组件 - Fluent Design风格的组合框
ComboBox {
    id: control
    
    // 基本尺寸
    implicitWidth: 200
    implicitHeight: 36
    
    // 背景样式
    background: Rectangle {
        border.width: control.hovered || control.focused ? 2 : 1
        border.color: control.focused ? "#0078d4" : control.hovered ? "#0078d4" : "#e0e0e0"
        radius: 4
        color: control.background
        
        // 右侧指示器区域
        Rectangle {
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            width: 36
            height: 36
            color: "transparent"
            
            // 下拉箭头
            PathView {
                id: indicator
                model: 1
                delegate: Image {
                    source: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24'><path fill='%23666666' d='M7 10l5 5 5-5z'/></svg>"
                    anchors.centerIn: parent
                }
                pathItemCount: 1
                path: Path {
                    startX: 0; startY: 0
                    PathLine { x: 0; y: 0 }
                }
            }
        }
        
        // 聚焦时的动画效果
        Behavior on border.color {
            ColorAnimation { duration: 200 }
        }
    }
    
    // 内容项样式
    contentItem: Text {
        text: control.displayText
        font.pointSize: 14
        font.family: "Microsoft YaHei"
        color: control.enabled ? "#333" : "#999"
        horizontalAlignment: Text.AlignLeft
        verticalAlignment: Text.AlignVCenter
        leftPadding: 10
        rightPadding: 36  // 为右侧指示器留出空间
    }
    
    // 弹出菜单样式
    popup: Popup {
        y: control.height
        width: control.width
        implicitHeight: contentItem.implicitHeight + 20
        padding: 10
        
        contentItem: ListView {
            id: listView
            clip: true
            model: control.delegateModel
            currentIndex: control.highlightedIndex
            
            delegate: ItemDelegate {
                width: listView.width
                contentItem: Text {
                    text: control.textRole ? (Array.isArray(control.model) ? modelData[control.textRole] : model[control.textRole]) : modelData
                    font.pointSize: 14
                    font.family: "Microsoft YaHei"
                    color: control.enabled ? "#333" : "#999"
                    horizontalAlignment: Text.AlignLeft
                }
                highlighted: control.highlightedIndex === index
                
                // 选中项的样式
                background: Rectangle {
                    color: highlighted ? "#e6f3ff" : "transparent"
                    border.color: highlighted ? "#0078d4" : "transparent"
                    border.width: highlighted ? 1 : 0
                }
            }
            
            ScrollIndicator.vertical: ScrollIndicator {}
        }
        
        // 弹出菜单背景
        background: Rectangle {
            border.color: "#e0e0e0"
            border.width: 1
            radius: 4
            color: "#ffffff"
            
            // 阴影效果
            layer.enabled: true
            layer.effect: DropShadow {
                color: "rgba(0, 0, 0, 0.2)"
                radius: 4
                samples: 8
                offset.x: 0
                offset.y: 2
            }
        }
    }
    
    // 鼠标区域设置
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onClicked: control.open()
    }
}