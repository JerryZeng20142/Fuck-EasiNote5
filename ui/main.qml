import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3
import "RinUI" // 导入ui/RinUI目录下的组件

ApplicationWindow {
    id: mainWindow
    visible: true
    width: 800
    height: 600
    title: "Fuck-EasiNote5 - 希沃白板5修改工具"
    
    // 主题属性绑定到Backend
    property bool isDarkMode: backend.isDarkMode
    
    // 根据主题动态设置颜色
    property color primaryColor: isDarkMode ? "#0078d4" : "#0078d4"
    property color textPrimaryColor: isDarkMode ? "#ffffff" : "#333333"
    property color textSecondaryColor: isDarkMode ? "#cccccc" : "#666666"
    property color surfaceColor: isDarkMode ? "#1e1e1e" : "#ffffff"
    property color borderColor: isDarkMode ? "#333333" : "#e0e0e0"
    property color backgroundColor: isDarkMode ? "#121212" : "#f5f5f5"
    
    // 连接Backend信号
    Connections {
        target: backend
        function onThemeChanged(theme) {
            mainWindow.isDarkMode = theme === "dark"
        }
    }
    
    // 窗口背景色
    color: backgroundColor
    
    // 主布局
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        
        // 标题区域
        RowLayout {
            Layout.fillWidth: true
            
            Text {
                text: "Fuck-EasiNote5"
                font.pointSize: 24
                font.bold: true
                color: mainWindow.primaryColor
            }
            
            Text {
                text: "v1.0.0"
                font.pointSize: 14
                color: mainWindow.textSecondaryColor
                Layout.alignment: Qt.AlignBottom
            }
        }
        
        // 状态显示区域
        RowLayout {
            Layout.fillWidth: true
            Layout.preferredHeight: 40
            spacing: 10
            
            Text {
                id: statusText
                text: "就绪"
                color: mainWindow.textPrimaryColor
                Layout.fillWidth: true
                verticalAlignment: Text.AlignVCenter
            }
            
            Button {
                text: mainWindow.isDarkMode ? "☀️ 亮色" : "🌙 暗色"
                onClicked: {
                    backend.toggleTheme()
                }
            }
        }
        
        // 希沃白板路径设置区域
        RowLayout {
            Layout.fillWidth: true
            Layout.preferredHeight: 40
            spacing: 10
            
            Text {
                text: "希沃白板路径:" 
                color: mainWindow.textPrimaryColor
                verticalAlignment: Text.AlignVCenter
            }
            
            // 使用基础组件创建输入框
            Rectangle {
                id: easiNotePathField
                Layout.fillWidth: true
                height: 30
                color: mainWindow.surfaceColor
                border.color: mainWindow.borderColor
                radius: 4
                
                TextInput {
                    id: pathInput
                    anchors.fill: parent
                    anchors.margins: 5
                    text: backend ? backend.getEasiNotePath() : ""
                    color: mainWindow.textPrimaryColor
                    focus: true
                    selectByMouse: true
                    onEditingFinished: {
                        backend.setEasiNotePath(pathInput.text)
                    }
                }
            }
            
            Button {
                text: "自动检测"
                onClicked: {
                    backend.autoDetectEasiNote()
                }
            }
        }
        
        // 功能卡片区域
        GridLayout {
            columns: 2
            Layout.fillWidth: true
            Layout.fillHeight: true
            
            // 第一个功能卡片 - 使用基础组件
            Rectangle {
                id: card1
                Layout.fillWidth: true
                Layout.preferredHeight: 200
                color: mainWindow.surfaceColor
                border.color: mainWindow.borderColor
                radius: 8
                
                ColumnLayout {
                    anchors.fill: parent
                    
                    // 卡片标题
                    Rectangle {
                        Layout.fillWidth: true
                        height: 40
                        color: mainWindow.primaryColor
                        radius: 8
                        
                        Text {
                            anchors.centerIn: parent
                            text: "基础功能修改"
                            color: "#ffffff"
                            font.bold: true
                        }
                    }
                    
                    // 卡片内容
                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 16
                        
                        Text {
                            text: "优化启动项、精简界面等基础功能修改"
                            color: mainWindow.textPrimaryColor
                            wrapMode: Text.WordWrap
                        }
                        
                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 10
                            Layout.alignment: Qt.AlignRight
                            
                            Button {
                                text: "优化启动"
                                Layout.preferredWidth: 100
                                onClicked: {
                                    backend.optimizeStartup()
                                }
                            }
                            
                            Button {
                                text: "精简界面"
                                Layout.preferredWidth: 100
                                onClicked: {
                                    backend.simplifyUI()
                                }
                            }
                        }
                    }
                }
            }
            
            // 第二个功能卡片 - 使用基础组件
            Rectangle {
                id: card2
                Layout.fillWidth: true
                Layout.preferredHeight: 200
                color: mainWindow.surfaceColor
                border.color: mainWindow.borderColor
                radius: 8
                
                ColumnLayout {
                    anchors.fill: parent
                    
                    // 卡片标题
                    Rectangle {
                        Layout.fillWidth: true
                        height: 40
                        color: mainWindow.primaryColor
                        radius: 8
                        
                        Text {
                            anchors.centerIn: parent
                            text: "高级功能设置"
                            color: "#ffffff"
                            font.bold: true
                        }
                    }
                    
                    // 卡片内容
                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 16
                        
                        Text {
                            text: "应用高级修改和管理资源"
                            color: mainWindow.textPrimaryColor
                            wrapMode: Text.WordWrap
                        }
                        
                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 10
                            Layout.alignment: Qt.AlignRight
                            
                            Button {
                                text: "应用修改"
                                Layout.preferredWidth: 100
                                onClicked: {
                                    backend.applyModifications()
                                }
                            }
                            
                            Button {
                                text: "管理资源"
                                Layout.preferredWidth: 100
                                onClicked: {
                                    backend.manageResources()
                                }
                            }
                        }
                    }
                }
            }
            
            // 第三个功能卡片 - 使用基础组件
            Rectangle {
                id: card3
                Layout.fillWidth: true
                Layout.preferredHeight: 200
                color: mainWindow.surfaceColor
                border.color: mainWindow.borderColor
                radius: 8
                
                ColumnLayout {
                    anchors.fill: parent
                    
                    // 卡片标题
                    Rectangle {
                        Layout.fillWidth: true
                        height: 40
                        color: mainWindow.primaryColor
                        radius: 8
                        
                        Text {
                            anchors.centerIn: parent
                            text: "配置文件管理"
                            color: "#ffffff"
                            font.bold: true
                        }
                    }
                    
                    // 卡片内容
                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 16
                        
                        Text {
                            text: "备份和恢复希沃白板的配置设置"
                            color: mainWindow.textPrimaryColor
                            wrapMode: Text.WordWrap
                        }
                        
                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 10
                            Layout.alignment: Qt.AlignRight
                            
                            Button {
                                text: "备份设置"
                                Layout.preferredWidth: 100
                                onClicked: {
                                    backend.backupSettings()
                                }
                            }
                            
                            Button {
                                text: "恢复设置"
                                Layout.preferredWidth: 100
                                onClicked: {
                                    backend.restoreSettings()
                                }
                            }
                        }
                    }
                }
            }
            
            // 第四个功能卡片 - 使用基础组件
            Rectangle {
                id: card4
                Layout.fillWidth: true
                Layout.preferredHeight: 200
                color: mainWindow.surfaceColor
                border.color: mainWindow.borderColor
                radius: 8
                
                ColumnLayout {
                    anchors.fill: parent
                    
                    // 卡片标题
                    Rectangle {
                        Layout.fillWidth: true
                        height: 40
                        color: mainWindow.primaryColor
                        radius: 8
                        
                        Text {
                            anchors.centerIn: parent
                            text: "备份与恢复"
                            color: "#ffffff"
                            font.bold: true
                        }
                    }
                    
                    // 卡片内容
                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 16
                        
                        Text {
                            text: "备份当前配置或恢复原始文件"
                            color: mainWindow.textPrimaryColor
                            wrapMode: Text.WordWrap
                        }
                        
                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 10
                            Layout.alignment: Qt.AlignRight
                            
                            Button {
                                text: "创建备份"
                                Layout.preferredWidth: 100
                                onClicked: {
                                    backend.createBackup()
                                }
                            }
                            
                            Button {
                                text: "恢复原始"
                                Layout.preferredWidth: 100
                                onClicked: {
                                    backend.restoreOriginal()
                                }
                            }
                        }
                    }
                }
            }
        }
        
        // 底部信息
        RowLayout {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignBottom
            
            Text {
                text: "© 2024 Fuck-EasiNote5"
                color: mainWindow.textSecondaryColor
            }
            
            Item {
                Layout.fillWidth: true
            }
            
            // 管理员权限检查
            Text {
                id: adminStatus
                text: backend && backend.checkAdminRights() ? "已获取管理员权限" : "需要管理员权限"
                color: backend && backend.checkAdminRights() ? "#4CAF50" : "#F44336"
                visible: false // 默认隐藏，需要时可显示
            }
            
            Button {
                text: "退出"
                Layout.preferredWidth: 80
                onClicked: {
                    console.log("退出按钮被点击")
                    Qt.quit()
                }
            }
        }
        
        // 监听状态变化
        Connections {
            target: backend
            function onStatusChanged(message) {
                statusText.text = message
            }
            
            function onMessageBox(title, content) {
                // 简单的消息框实现
                var msgBox = Qt.createQmlObject('import QtQuick.Controls 2.15; import QtQuick.Dialogs 1.3; MessageDialog { title: "' + title + '"; text: "' + content + '"; visible: true; standardButtons: StandardButton.Ok }', mainWindow)
            }
        }
    }
}