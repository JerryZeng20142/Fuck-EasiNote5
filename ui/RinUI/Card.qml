import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtGraphicalEffects 1.15
import "../RinUI" // 导入主题

// 卡片容器组件 - 优化版（更符合RinUI Fluent Design风格）
Rectangle {
    id: card
    
    // 自定义属性
    property string title: ""
    property bool hasHeader: false
    property bool hasShadow: true
    property int cardRadius: 8
    property bool darkMode: false
    
    // 使用主题颜色
    property var currentTheme: darkMode ? Theme {}.dark.Theme : Theme {}.light.Theme
    
    // 基本样式
    color: currentTheme.card
    radius: cardRadius
    border.width: 0 // 移除边框，使用阴影效果
    
    // 添加阴影效果
    layer.enabled: hasShadow
    layer.effect: DropShadow {
        color: currentTheme.shadow
        radius: 10
        samples: 20
        offset.x: 0
        offset.y: 4
    }
    
    // 鼠标悬停效果
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        
        onEntered: {
            card.y = card.y - 2
            card.layer.effect.opacity = 0.8
        }
        
        onExited: {
            card.y = card.y + 2
            card.layer.effect.opacity = 1.0
        }
    }
    
    // 内部布局
    ColumnLayout {
        anchors.fill: parent
        spacing: 0
        
        // 卡片头部
        Rectangle {
            id: header
            visible: hasHeader
            Layout.fillWidth: true
            height: 48
            color: "transparent"
            
            // 标题文本
            Text {
                anchors.left: parent.left
                anchors.leftMargin: 16
                anchors.verticalCenter: parent.verticalCenter
                text: card.title
                font.pointSize: 16
                font.family: "Microsoft YaHei"
                font.bold: true
                color: currentTheme.text
            }
        }
        
        // 内容区域
        Item {
            id: contentArea
            Layout.fillWidth: true
            Layout.fillHeight: true
            
            // 允许子元素填充内容区域
            default property alias contentChildren: contentArea.children
        }
    }
    
    // 组件尺寸提示
    implicitWidth: 300
    implicitHeight: 200
}