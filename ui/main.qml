import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import RinUI 1.0

FluentWindow {
    id: window
    width: 800
    height: 600
    title: "希沃白板5修改工具"
    visible: true
    
    // 确保导航栏显示在最上层
    navigationView.z: 9999
    navigationView.appLayerEnabled: true
    navigationView.navExpandWidth: 280
    navigationView.navMinimumExpandWidth: 900
    
    // 希沃白板检测相关属性
    property string detectionResult: "未检测到希沃白板安装路径"
    property bool detectionSuccess: false
    property bool isDetecting: false
    
    // 组件完成时的初始化
    Component.onCompleted: {
        // 延迟执行，确保EasiNoteDetector已经可用
        Qt.callLater(function() {
            if (typeof EasiNoteDetector !== 'undefined') {
                console.log("EasiNoteDetector已可用")
            } else {
                console.log("EasiNoteDetector不可用")
            }
        })
    }
    
    // 主内容区域
    Item {
        anchors.fill: parent
        
        // 顶部横幅
        Rectangle {
            id: topBanner
            width: parent.width
            height: 150
            color: Utils.colors.primaryColor
            anchors.top: parent.top
            anchors.left: parent.left
            z: 1
            
            Column {
                anchors.centerIn: parent
                spacing: 10
                
                Text {
                    text: "希沃白板5修改工具"
                    font.pixelSize: 32
                    font.bold: true
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                }
                
                Text {
                    text: "轻松修改希沃白板5配置，解锁更多功能"
                    font.pixelSize: 16
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                }
            }
        }
        
        // 检测区域
        Rectangle {
            id: detectionArea
            width: parent.width - 60
            height: 200
            color: Utils.colors.cardColor
            radius: 10
            anchors.top: topBanner.bottom
            anchors.left: parent.left
            anchors.topMargin: 30
            anchors.leftMargin: 30
            z: 0
            
            Column {
                anchors.fill: parent
                spacing: 20
                padding: 20
                
                Text {
                    text: "希沃白板安装路径"
                    font.pixelSize: 20
                    font.bold: true
                    color: Utils.colors.textColor
                }
                
                // 检测结果显示和操作按钮（一排布局）
                RowLayout {
                    width: parent.width
                    spacing: 10
                    
                    // 文本框
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 40
                        color: Utils.colors.cardColor
                        border.color: detectionSuccess ? "#4ade80" : detectionSuccess === false ? "#f87171" : Utils.colors.borderColor
                        border.width: 2
                        radius: 8
                        
                        TextInput {
                            anchors.fill: parent
                            anchors.margins: 10
                            text: detectionResult
                            font.pixelSize: 14
                            color: Utils.colors.textColor
                            selectByMouse: true
                            readOnly: false
                        }
                    }
                    
                    // 操作按钮
                    Button {
                        text: isDetecting ? "检测中..." : "自动检测"
                        onClicked: {
                            isDetecting = true
                            detectionResult = "正在检测希沃白板安装路径..."
                            detectionSuccess = false
                            
                            // 调用检测器
                            EasiNoteDetector.detect_easinote_path()
                            
                            // 使用定时器模拟异步检测结果
                            Qt.callLater(function() {
                                // 这里应该通过信号获取真实结果
                                // 暂时使用模拟数据
                                detectionResult = "C:\\Program Files (x86)\\Seewo\\EasiNote5"
                                detectionSuccess = true
                                isDetecting = false
                            })
                        }
                        enabled: !isDetecting
                        Layout.preferredWidth: 120
                    }
                    
                    Button {
                        text: "手动选择"
                        onClicked: {
                            // 使用FileDialogManager选择路径
                            var selectedPath = FileDialogManager.selectFolder()
                            if (selectedPath) {
                                detectionResult = selectedPath
                                detectionSuccess = true
                                // 调用检测器的selectPath方法
                                EasiNoteDetector.selectPath(selectedPath)
                            } else {
                                console.log("选择路径已取消")
                            }
                        }
                        enabled: !isDetecting
                        Layout.preferredWidth: 120
                    }
                }
            }
        }
        
        // 功能入口区域
        Rectangle {
            id: functionArea
            width: parent.width - 60
            height: 250
            color: Utils.colors.cardColor
            radius: 10
            anchors.top: detectionArea.bottom
            anchors.left: parent.left
            anchors.topMargin: 30
            anchors.leftMargin: 30
            z: 2
            
            Column {
                anchors.fill: parent
                spacing: 20
                padding: 20
                
                Text {
                    text: "功能菜单"
                    font.pixelSize: 20
                    font.bold: true
                    color: Utils.colors.textColor
                }
                
                // 功能按钮网格
                Grid {
                    width: parent.width
                    columns: 2
                    spacing: 15
                    
                    // 功能按钮1
                    Button {
                        text: "修改配置"
                        width: (parent.width - 15) / 2
                        height: 80
                        enabled: detectionSuccess
                        onClicked: {
                            console.log("修改配置功能")
                        }
                    }
                    
                    // 功能按钮2
                    Button {
                        text: "备份数据"
                        width: (parent.width - 15) / 2
                        height: 80
                        enabled: detectionSuccess
                        onClicked: {
                            console.log("备份数据功能")
                        }
                    }
                    
                    // 功能按钮3
                    Button {
                        text: "恢复数据"
                        width: (parent.width - 15) / 2
                        height: 80
                        enabled: detectionSuccess
                        onClicked: {
                            console.log("恢复数据功能")
                        }
                    }
                    
                    // 功能按钮4
                    Button {
                        text: "关于软件"
                        width: (parent.width - 15) / 2
                        height: 80
                        onClicked: {
                            console.log("关于软件功能")
                        }
                    }
                }
            }
        }
    }
}