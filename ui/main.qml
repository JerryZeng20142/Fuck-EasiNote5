import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15

ApplicationWindow {
    id: mainWindow
    visible: true
    width: 800
    height: 600
    title: "Fuck-EasiNote5 - 希沃白板5修改工具"
    
    // 主题属性绑定到Backend
    property bool isDarkMode: backend ? backend.isDarkMode : false
    
    // 使用RinUI主题系统 - 直接引用Theme组件中的属性
    property var themeColors: {
        "primary": isDarkMode ? "#0078d4" : "#0078d4",
        "text": isDarkMode ? "#ffffff" : "#333333",
        "textSecondary": isDarkMode ? "#cccccc" : "#666666",
        "surface": isDarkMode ? "#252525" : "#ffffff",
        "border": isDarkMode ? "#404040" : "#e0e0e0",
        "background": isDarkMode ? "#1a1a1a" : "#f5f5f5",
        "primaryLight": isDarkMode ? "#106ebe" : "#106ebe",
        "primaryDark": isDarkMode ? "#005a9e" : "#005a9e",
        "accent": isDarkMode ? "#e74c3c" : "#e74c3c",
        "accentLight": isDarkMode ? "#d13438" : "#d13438",
        "accentDark": isDarkMode ? "#b31919" : "#b31919",
        "shadow": isDarkMode ? "rgba(0, 0, 0, 0.3)" : "rgba(0, 0, 0, 0.1)",
        "radius": 4
    }
    
    property var currentTheme: themeColors
    property color primaryColor: currentTheme.primary
    property color textPrimaryColor: currentTheme.text
    property color textSecondaryColor: currentTheme.textSecondary
    property color surfaceColor: currentTheme.surface
    property color borderColor: currentTheme.border
    property color backgroundColor: currentTheme.background
    
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
        Layout.fillWidth: true
        Layout.fillHeight: true
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
                background: Rectangle {

                    radius: mainWindow.currentTheme.radius
                }
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
            
            // 使用主题样式的输入框
            Rectangle {
                id: easiNotePathField
                Layout.fillWidth: true
                height: 36
                color: mainWindow.surfaceColor
                border.color: mainWindow.borderColor
                radius: mainWindow.currentTheme.radius
                
                TextInput {
                    id: pathInput
                    anchors.fill: parent
                    anchors.margins: 10
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
                background: Rectangle {

                    radius: mainWindow.currentTheme.radius
                }
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
            
            // 第一个功能卡片
            Rectangle {
                id: card1
                Layout.fillWidth: true
                Layout.preferredHeight: 200
                color: mainWindow.surfaceColor
                border.color: mainWindow.borderColor
                border.width: 1
                radius: mainWindow.currentTheme.radius
                
                ColumnLayout {
                    anchors.fill: parent
                    spacing: 12
                    
                    Text {
                        Layout.fillWidth: true
                        text: "基础功能修改"
                        color: mainWindow.textPrimaryColor
                        font.pixelSize: 16
                        font.bold: true
                        padding: 12
                    }
                    
                    ColumnLayout {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        anchors.margins: 16
                        spacing: 16
                        
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
                                // primary属性已移除，使用默认样式
                                // darkMode属性已移除，使用默认样式
                                Layout.preferredWidth: 100
                                onClicked: {
                                    backend.optimizeStartup()
                                }
                            }
                
                Button {
                    text: "精简界面"
                    // darkMode属性已移除，使用默认样式
                    Layout.preferredWidth: 100
                    onClicked: {
                        backend.simplifyUI()
                    }
                }
                        }
                    }
                }
            }
            
            // 第二个功能卡片
            Rectangle {
                id: card2
                Layout.fillWidth: true
                Layout.preferredHeight: 200
                color: mainWindow.surfaceColor
                border.color: mainWindow.borderColor
                border.width: 1
                radius: mainWindow.currentTheme.radius
                
                ColumnLayout {
                    anchors.fill: parent
                    spacing: 12
                    
                    Text {
                        Layout.fillWidth: true
                        text: "高级功能设置"
                        color: mainWindow.textPrimaryColor
                        font.pixelSize: 16
                        font.bold: true
                        padding: 12
                    }
                    
                    ColumnLayout {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        anchors.margins: 16
                        spacing: 16
                        
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
                                // primary属性已移除，使用默认样式
                                // darkMode属性已移除，使用默认样式
                                Layout.preferredWidth: 100
                                onClicked: {
                                    backend.applyModifications()
                                }
                }
                
                Button {
                    text: "管理资源"
                    // darkMode属性已移除，使用默认样式
                    Layout.preferredWidth: 100
                    onClicked: {
                        backend.manageResources()
                    }
                }
                        }
                    }
                }
            }
            
            // 第三个功能卡片
            Rectangle {
                id: card3
                Layout.fillWidth: true
                Layout.preferredHeight: 200
                color: mainWindow.surfaceColor
                border.color: mainWindow.borderColor
                border.width: 1
                radius: mainWindow.currentTheme.radius
                
                ColumnLayout {
                    anchors.fill: parent
                    spacing: 12
                    
                    Text {
                        Layout.fillWidth: true
                        text: "配置文件管理"
                        color: mainWindow.textPrimaryColor
                        font.pixelSize: 16
                        font.bold: true
                        padding: 12
                    }
                    
                    ColumnLayout {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    anchors.margins: 16
                    spacing: 16
                        
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
                                // primary属性已移除，使用默认样式
                                // darkMode属性已移除，使用默认样式
                                Layout.preferredWidth: 100
                                onClicked: {
                                    backend.backupSettings()
                                }
                }
                
                Button {
                    text: "恢复设置"
                    darkMode: mainWindow.isDarkMode
                    Layout.preferredWidth: 100
                    onClicked: {
                        backend.restoreSettings()
                    }
                }
                        }
                    }
                }
            }
            
            // 第四个功能卡片
            Rectangle {
                id: card4
                Layout.fillWidth: true
                Layout.preferredHeight: 200
                color: mainWindow.surfaceColor
                border.color: mainWindow.borderColor
                border.width: 1
                radius: mainWindow.currentTheme.radius
                
                ColumnLayout {
                    anchors.fill: parent
                    spacing: 12
                    
                    Text {
                        Layout.fillWidth: true
                        text: "备份与恢复"
                        color: mainWindow.textPrimaryColor
                        font.pixelSize: 16
                        font.bold: true
                        padding: 12
                    }
                    
                    ColumnLayout {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    anchors.margins: 16
                    spacing: 16
                        
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
                                // primary和darkMode属性已移除，使用默认样式
                                Layout.preferredWidth: 100
                                onClicked: {
                                    backend.createBackup()
                                }
                }
                
                Button {
                    text: "恢复原始"
                    darkMode: mainWindow.isDarkMode
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
                // primary和darkMode属性已移除，使用默认样式
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
                // 自定义消息框实现
                var msgBox = Qt.createQmlObject('import QtQuick 2.15; import QtQuick.Controls 2.15; import QtQuick.Layouts 1.15; Rectangle { id: messageBox; anchors.centerIn: parent; width: 400; height: 200; color: "white"; radius: 8; border.color: "#0078d4"; z: 100; ColumnLayout { anchors.fill: parent; spacing: 10; Text { text: "' + title + '"; font.bold: true; font.pointSize: 16; color: "#333333"; Layout.fillWidth: true; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter; padding: 10; } Text { text: "' + content + '"; color: "#666666"; wrapMode: Text.WordWrap; Layout.fillWidth: true; Layout.fillHeight: true; padding: Qt.rect(20, 0, 20, 0); } Button { text: "确定"; background: Rectangle { color: "#0078d4"; radius: 4; } color: "white"; Layout.alignment: Qt.AlignRight; onClicked: messageBox.destroy(); } } }', mainWindow)
            }
        }
    }
}