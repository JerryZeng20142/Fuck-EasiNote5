import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "./RinUI" as RinUI

Window {
    visible: true
    width: 800
    height: 600
    title: "希沃白板5修改工具"
    minimumWidth: 600
    minimumHeight: 400
    
    // 检查是否有管理员权限
    Component.onCompleted: {
        if (!backend.checkAdminRights()) {
            backend.messageBox("权限警告", "建议以管理员权限运行此程序以确保所有功能正常工作")
        }
    }
    
    // 主布局
    Rectangle {
        anchors.fill: parent
        color: "#f5f5f5"
        
        // 标题栏
        Rectangle {
            width: parent.width
            height: 50
            color: "#0078d4"
            
            RowLayout {
                anchors.fill: parent
                anchors.margins: 10
                
                Text {
                    text: "希沃白板5修改工具" + " v" + backend.getConfigValue("app.version")
                    color: "white"
                    font.pointSize: 16
                    font.bold: true
                }
            }
        }
        
        // 标签页
        TabView {
            anchors.top: parent.top
            anchors.topMargin: 50
            anchors.bottom: statusBar.top
            anchors.left: parent.left
            anchors.right: parent.right
            
            // 主界面标签页
            Tab {
                title: "主界面"
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 20
                    spacing: 20
                    
                    // 希沃白板路径设置
                    GroupBox {
                        title: "希沃白板安装路径"
                        Layout.fillWidth: true
                        
                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 10
                            spacing: 10
                            
                            TextField {
                                id: pathField
                                text: backend.getEasiNotePath()
                                Layout.fillWidth: true
                                onEditingFinished: {
                                    backend.setEasiNotePath(text)
                                }
                            }
                            
                            Button {
                                text: "浏览..."
                                onClicked: {
                                    // 实际项目中需要实现文件对话框
                                    backend.messageBox("提示", "浏览功能正在开发中")
                                }
                            }
                            
                            Button {
                                text: "自动检测"
                                onClicked: {
                                    backend.autoDetectEasiNote()
                                }
                            }
                        }
                    }
                    
                    // 操作按钮
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 20
                        
                        Button {
                            text: "创建备份"
                            Layout.fillWidth: true
                            onClicked: {
                                backend.createBackup()
                            }
                        }
                        
                        Button {
                            text: "应用修改"
                            Layout.fillWidth: true
                            onClicked: {
                                backend.applyModifications()
                            }
                        }
                        
                        Button {
                            text: "恢复原始"
                            Layout.fillWidth: true
                            onClicked: {
                                backend.restoreOriginal()
                            }
                        }
                    }
                }
            }
            
            // 功能修改标签页
            Tab {
                title: "功能修改"
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.centerIn: parent
                    spacing: 20
                    
                    Text {
                        text: "功能修改模块正在开发中..."
                        font.pointSize: 14
                        color: "#666"
                    }
                    
                    Text {
                        text: "请稍后再试"
                        color: "#999"
                    }
                }
            }
            
            // 设置标签页
            Tab {
                title: "设置"
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 20
                    spacing: 20
                    
                    GroupBox {
                        title: "界面设置"
                        Layout.fillWidth: true
                        
                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 10
                            spacing: 10
                            
                            Text {
                                text: "主题:"
                                verticalAlignment: Text.AlignVCenter
                            }
                            
                            ComboBox {
                                id: themeCombo
                                model: ["light", "dark"]
                                currentIndex: themeCombo.find(backend.getConfigValue("gui.theme"))
                                Layout.fillWidth: true
                            }
                        }
                    }
                    
                    Button {
                        text: "保存设置"
                        Layout.alignment: Qt.AlignHCenter
                        onClicked: {
                            backend.setConfigValue("gui.theme", themeCombo.currentText)
                            backend.messageBox("成功", "设置已保存")
                        }
                    }
                }
            }
            
            // 关于标签页
            Tab {
                title: "关于"
                
                ColumnLayout {
                    anchors.centerIn: parent
                    spacing: 15
                    
                    Text {
                        text: backend.getConfigValue("app.name")
                        font.pointSize: 20
                        font.bold: true
                        color: "#333"
                    }
                    
                    Text {
                        text: "版本: " + backend.getConfigValue("app.version")
                        color: "#666"
                    }
                    
                    Text {
                        text: "作者: " + backend.getConfigValue("app.author")
                        color: "#666"
                    }
                    
                    Text {
                        text: "希沃白板5修改工具，支持各种自定义设置和功能增强。"
                        color: "#666"
                        wrapMode: Text.WordWrap
                        width: 300
                        horizontalAlignment: Text.AlignHCenter
                    }
                    
                    Text {
                        text: "使用此工具风险自负，请确保备份原始文件。"
                        color: "#999"
                        wrapMode: Text.WordWrap
                        width: 300
                        horizontalAlignment: Text.AlignHCenter
                    }
                }
            }
        }
        
        // 状态栏
        Rectangle {
            id: statusBar
            anchors.bottom: parent.bottom
            width: parent.width
            height: 30
            color: "#e0e0e0"
            
            Text {
                id: statusText
                anchors.fill: parent
                anchors.margins: 5
                text: "就绪"
                font.pointSize: 12
                color: "#666"
                verticalAlignment: Text.AlignVCenter
            }
        }
    }
    
    // 监听后端信号
    Connections {
        target: backend
        
        function onStatusChanged(text) {
            statusText.text = text
        }
        
        function onEasiNotePathChanged(path) {
            pathField.text = path
        }
    }
}