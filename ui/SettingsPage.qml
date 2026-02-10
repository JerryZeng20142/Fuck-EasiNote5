import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import RinUI 1.0

Item {
    // 主题设置属性
    property string currentTheme: "auto"
    
    // 布局容器
    Column {
        anchors.fill: parent
        spacing: 20
        padding: 30
        
        // 页面标题
        Text {
            text: "设置"
            font.pixelSize: 28
            font.bold: true
            color: Utils.colors.textColor
        }
        
        // 主题设置卡片
        Rectangle {
            width: parent.width
            height: 300
            color: Utils.colors.cardColor
            radius: 10
            
            Column {
                anchors.fill: parent
                spacing: 0
                
                // 卡片标题
                Rectangle {
                    width: parent.width
                    height: 50
                    color: "transparent"
                    radius: 10
                    
                    Text {
                        anchors.left: parent.left
                        anchors.leftMargin: 20
                        anchors.verticalCenter: parent.verticalCenter
                        text: "主题设置"
                        font.pixelSize: 18
                        font.bold: true
                        color: Utils.colors.textColor
                    }
                }
                
                // 主题选项容器
                Column {
                    anchors.fill: parent
                    anchors.topMargin: 20
                    anchors.leftMargin: 20
                    anchors.rightMargin: 20
                    spacing: 25
                    
                    // 主题选择组合框
                    RowLayout {
                        width: parent.width
                        spacing: 15
                        
                        // 选项文本和描述
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 5
                            
                            Text {
                                text: "主题选择"
                                font.pixelSize: 16
                                color: Utils.colors.textColor
                            }
                            
                            Text {
                                text: "选择应用程序的主题样式"
                                font.pixelSize: 12
                                color: Utils.colors.textColor
                                opacity: 0.7
                                wrapMode: Text.WordWrap
                            }
                        }
                        
                        // 组合框
                        ComboBox {
                            id: themeComboBox
                            Layout.preferredWidth: 150
                            
                            // 主题选项模型
                            model: [
                                { text: "系统默认", value: "auto" },
                                { text: "浅色模式", value: "light" },
                                { text: "深色模式", value: "dark" }
                            ]
                            
                            // 显示文本
                            textRole: "text"
                            
                            // 选择处理
                            onActivated: {
                                // 获取选中的主题值
                                let theme = model[index].value;
                                setTheme(theme);
                            }
                            
                            // 键盘可访问性
                            focusPolicy: Qt.StrongFocus
                        }
                    }
                }
            }
        }
    }
    
    // 设置主题函数
    function setTheme(theme) {
        currentTheme = theme
        
        // 更新组合框选中项
        for (let i = 0; i < themeComboBox.model.length; i++) {
            if (themeComboBox.model[i].value === theme) {
                themeComboBox.currentIndex = i;
                break;
            }
        }
        
        // 调用Python端的主题设置函数
        ThemeManager.setTheme(theme)
    }
    
    // 初始化主题设置
    Component.onCompleted: {
        // 从Python端获取当前主题设置
        currentTheme = ThemeManager.getCurrentTheme()
        
        // 更新组合框选中项
        for (let i = 0; i < themeComboBox.model.length; i++) {
            if (themeComboBox.model[i].value === currentTheme) {
                themeComboBox.currentIndex = i;
                break;
            }
        }
    }
}