import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQml.Models 2.15
import QtQuick.Layouts 1.15
// 移除对QtQuick.Dialogs的依赖，因为当前PySide6版本可能不支持

// 导入Rin-UI组件库
import RinUI 1.0

Window {
    id: mainWindow
    width: 900
    height: 700
    visible: true
    title: "希沃白板5修改工具"
    color: "#f0f0f0"
    
    // 状态栏消息
    property string statusMessage: "就绪"
    
    // 日志内容
    property string logContent: ""
    
    // 选中的音频文件路径
    property string selectedAudioPath: ""
    
    // 游戏文件列表模型
    property variant gameFilesModel: null
    
    // 配置对话框相关属性
    property bool showConfigDialog: false
    property string easinotePath: ""
    
    // 当Python后端更新游戏文件列表时的处理
    function onGameFilesUpdated(model) {
        gameFilesModel = model
    }
    
    // 浏览音频文件的函数
    function browseAudioFile() {
        // 使用QML文件对话框
        fileDialog.open()
    }
    
    // 文件对话框
    FileDialog {
        id: fileDialog
        title: "选择音频文件"
        nameFilters: ["音频文件 (*.mp3 *.wav *.ogg *.flac)", "MP3文件 (*.mp3)", "WAV文件 (*.wav)", "OGG文件 (*.ogg)", "FLAC文件 (*.flac)"]
        selectExisting: true
        onAccepted: {
            selectedAudioPath = fileDialog.fileUrl.replace("file:///", "").replace(/\//g, "\\")
            setAudioPathFromQml(selectedAudioPath)
        }
    }
    
    // 配置对话框
    Dialog {
        id: configDialog
        visible: showConfigDialog
        title: "希沃白板5配置"
        modal: true
        
        ColumnLayout {
            width: 500
            padding: 16
            spacing: 16
            
            Label {
                text: "希沃白板5安装目录:"
                font.weight: Font.Bold
            }
            
            RowLayout {
                width: parent.width
                spacing: 8
                
                TextField {
                    id: configPathField
                    text: easinotePath
                    placeholderText: "请选择希沃白板5安装目录"
                    Layout.fillWidth: true
                }
                
                Button {
                    text: "浏览"
                    onClicked: {
                        // 使用QML文件夹对话框
                        folderDialog.open()
                    }
                }
            }
            
            FolderDialog {
                id: folderDialog
                title: "选择希沃白板5安装目录"
                selectFolder: true
                initialFolder: easinotePath
                onAccepted: {
                    configPathField.text = folderDialog.fileUrl.replace("file:///", "").replace(/\//g, "\\")
                }
            }
            
            RowLayout {
                Layout.alignment: Qt.AlignRight
                spacing: 8
                
                Button {
                    text: "取消"
                    onClicked: {
                        showConfigDialog = false
                    }
                }
                
                Button {
                    text: "确定"
                    onClicked: {
                        setEasinotePath(configPathField.text)
                        showConfigDialog = false
                        backend.refreshGameFiles()
                    }
                }
            }
        }
    }
    
    // 主布局
    ColumnLayout {
        anchors.fill: parent
        spacing: 0
        
        // 标题栏
        Rectangle {
            color: "#3a7bd5"
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            
            RowLayout {
                anchors.fill: parent
                padding: 10
                spacing: 10
                
                Label {
                    text: "希沃白板5修改工具"
                    font.pixelSize: 18
                    font.bold: true
                    color: "white"
                }
                
                Item {
                    Layout.fillWidth: true
                }
                
                Button {
                    text: "配置路径"
                    onClicked: {
                        easinotePath = getEasinotePath()
                        showConfigDialog = true
                    }
                }
            }
        }
        
        // 主要内容区域
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "#f0f0f0"
            
            RowLayout {
                anchors.fill: parent
                spacing: 10
                padding: 10
                
                // 左侧面板 - 游戏文件列表
                ColumnLayout {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    spacing: 8
                    
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 40
                        color: "white"
                        radius: 4
                        
                        RowLayout {
                            anchors.fill: parent
                            padding: 8
                            spacing: 8
                            
                            Label {
                                text: "游戏文件列表"
                                font.weight: Font.Bold
                            }
                            
                            Item {
                                Layout.fillWidth: true
                            }
                            
                            Button {
                                text: "刷新"
                                onClicked: {
                                    backend.refreshGameFiles()
                                }
                            }
                        }
                    }
                    
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        color: "white"
                        radius: 4
                        
                        ListView {
                            id: gameFilesList
                            anchors.fill: parent
                            model: gameFilesModel
                            spacing: 2
                            clip: true
                            
                            delegate: Rectangle {
                                width: parent.width
                                height: 40
                                color: gameFilesList.currentIndex === index ? "#e3f2fd" : "white"
                                border.color: "#e0e0e0"
                                border.width: 1
                                
                                RowLayout {
                                    anchors.fill: parent
                                    padding: 8
                                    spacing: 8
                                    
                                    Label {
                                        text: model.display
                                        Layout.fillWidth: true
                                        elide: Text.ElideRight
                                    }
                                }
                                
                                MouseArea {
                                    anchors.fill: parent
                                    onClicked: {
                                        gameFilesList.currentIndex = index
                                        // 获取完整的文件路径（存储在第二列）
                                        var fileModel = gameFilesModel
                                        if (fileModel && fileModel.rowCount() > index) {
                                            var filePath = fileModel.data(fileModel.index(index, 1))
                                            backend.selectGameFile(filePath)
                                        }
                                    }
                                    onDoubleClicked: {
                                        var fileModel = gameFilesModel
                                        if (fileModel && fileModel.rowCount() > index) {
                                            var filePath = fileModel.data(fileModel.index(index, 1))
                                            backend.showFileInfo(filePath)
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                
                // 右侧面板 - 操作区
                ColumnLayout {
                    Layout.preferredWidth: 320
                    Layout.fillHeight: true
                    spacing: 8
                    
                    // 音频选择区域
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 120
                        color: "white"
                        radius: 4
                        
                        ColumnLayout {
                            anchors.fill: parent
                            padding: 10
                            spacing: 10
                            
                            Label {
                                text: "选择音频文件"
                                font.weight: Font.Bold
                            }
                            
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 8
                                
                                TextField {
                                    id: audioPathField
                                    text: selectedAudioPath
                                    placeholderText: "未选择音频文件"
                                    Layout.fillWidth: true
                                    readOnly: true
                                }
                                
                                Button {
                                    text: "浏览"
                                    onClicked: {
                                        browseAudioFile()
                                    }
                                }
                            }
                            
                            Button {
                                text: "预览音频"
                                onClicked: {
                                    backend.previewAudio()
                                }
                            }
                        }
                    }
                    
                    // 操作按钮区域
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 160
                        color: "white"
                        radius: 4
                        
                        ColumnLayout {
                            anchors.fill: parent
                            padding: 10
                            spacing: 10
                            
                            Label {
                                text: "操作"
                                font.weight: Font.Bold
                            }
                            
                            Button {
                                text: "修改背景音乐"
                                Layout.fillWidth: true
                                Layout.preferredHeight: 40
                                onClicked: {
                                    backend.modifyBgm()
                                }
                            }
                            
                            Button {
                                text: "恢复默认背景音乐"
                                Layout.fillWidth: true
                                Layout.preferredHeight: 40
                                onClicked: {
                                    backend.restoreBgm()
                                }
                            }
                        }
                    }
                    
                    // 日志区域
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        color: "white"
                        radius: 4
                        
                        ColumnLayout {
                            anchors.fill: parent
                            padding: 10
                            spacing: 10
                            
                            Label {
                                text: "操作日志"
                                font.weight: Font.Bold
                            }
                            
                            TextArea {
                                text: backend.logContent
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                readOnly: true
                                wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                                font.family: "Consolas, Monaco, 'Courier New'"
                                font.pixelSize: 12
                                
                                ScrollBar.vertical: ScrollBar {}
                            }
                        }
                    }
                }
            }
        }
        
        // 状态栏
        Rectangle {
            color: "#e0e0e0"
            Layout.fillWidth: true
            Layout.preferredHeight: 30
            
            RowLayout {
                anchors.fill: parent
                padding: 5
                
                Label {
                    text: backend.statusMessage
                    elide: Text.ElideRight
                    Layout.fillWidth: true
                }
                
                Label {
                    text: "版本: 0.1.0"
                }
            }
        }
    }
    
    // 连接后端信号到QML
    Connections {
        target: backend
        function onStatusMessageChanged(message) {
            mainWindow.statusMessage = message
        }
        function onLogContentChanged(content) {
            mainWindow.logContent = content
        }
        function onAudioPathChanged(path) {
            mainWindow.selectedAudioPath = path
        }
        function onGameFilesUpdated(model) {
            mainWindow.onGameFilesUpdated(model)
        }
    }
    
    // 初始化
    Component.onCompleted: {
        // 获取配置路径
        mainWindow.easinotePath = getEasinotePath()
        // 刷新游戏文件列表
        backend.refreshGameFiles()
    }
}