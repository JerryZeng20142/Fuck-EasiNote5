import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15

ApplicationWindow {
    id: mainWindow
    visible: true
    minimumWidth: 850
    minimumHeight: 650
    width: 850 // 进一步减小默认宽度
    height: 650 // 进一步减小高度
    title: "希沃白板5小游戏音乐修改"
    
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
        Layout.alignment: Qt.AlignCenter
        anchors.margins: 20
        
        // 标题区域
        RowLayout {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignHCenter
            spacing: 10
            
            Text {
                text: "希沃白板5小游戏音乐修改"
                font.pointSize: 24
                font.bold: true
                color: mainWindow.primaryColor
            }
            
            Text {
                text: "v1.0.0"
                font.pointSize: 14
                color: mainWindow.textSecondaryColor
                Layout.alignment: Qt.AlignVCenter
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
                onClicked: {
                    backend.autoDetectEasiNote()
                }
            }
        }
        
        // 功能卡片区域
        GridLayout {
            // 根据窗口宽度自动调整列数
            columns: mainWindow.width < 900 ? 1 : 2
            rowSpacing: 20
            columnSpacing: 20
            Layout.fillWidth: true
            Layout.preferredHeight: mainWindow.height * 0.6 // 自适应高度
            Layout.alignment: Qt.AlignHCenter | Qt.AlignTop // 水平居中且顶部对齐
            
            // 第一个功能卡片已移除
            
            // 第二个功能卡片
            Rectangle {
                id: card2
                Layout.fillWidth: true
                Layout.minimumWidth: 350
                Layout.maximumWidth: 800 // 设置合理的最大宽度
                Layout.preferredHeight: 180
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
                            text: "管理资源"
                            color: mainWindow.textPrimaryColor
                            wrapMode: Text.WordWrap
                        }
                        
                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 10
                            Layout.alignment: Qt.AlignHCenter
                            
                            Button {
                                text: "管理资源"
                                Layout.preferredWidth: 130
                                onClicked: {
                                    backend.manageResources();
                                    resourceWindow.visible = true;
                                    resourceWindow.updateResourceList();
                                }
                            }
                        }
                    }
                }
            }
            
            // 第三个功能卡片已移除（配置文件管理）
            
            // 第四个功能卡片
            Rectangle {
                id: card4
                Layout.fillWidth: true
                Layout.minimumWidth: 350
                Layout.maximumWidth: 800 // 设置合理的最大宽度
                Layout.preferredHeight: 180
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
                            Layout.alignment: Qt.AlignHCenter
                            
                            Button {
                                text: "创建备份"
                                Layout.preferredWidth: 130
                                onClicked: {
                                    backend.createBackup()
                                }
                            }
                            
                            Button {
                                text: "恢复原始"
                                Layout.preferredWidth: 130
                                onClicked: {
                                    backend.restoreOriginal()
                                }
                            }
                        }
                    }
                }
            }
        }
        
        // 底部信息区域已移除
        
        // 监听状态变化
        Connections {
            target: backend
            function onStatusChanged(message) {
                statusText.text = message
            }
            
            function onMessageBox(title, content) {
                // 自定义消息框实现 - 适配主题
                var isDark = mainWindow.isDarkMode;
                var surfaceColor = isDark ? "#252525" : "#ffffff";
                var textColor = isDark ? "#ffffff" : "#333333";
                var secondaryTextColor = isDark ? "#cccccc" : "#666666";
                var primaryColor = "#0078d4";
                
                var msgBox = Qt.createQmlObject('import QtQuick 2.15; import QtQuick.Controls 2.15; import QtQuick.Layouts 1.15; Rectangle { id: messageBox; anchors.centerIn: parent; width: 400; height: 200; color: "' + surfaceColor + '"; radius: 8; border.color: "' + primaryColor + '"; z: 100; ColumnLayout { anchors.fill: parent; spacing: 10; Text { text: "' + title + '"; font.bold: true; font.pointSize: 16; color: "' + textColor + '"; Layout.fillWidth: true; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter; padding: 10; } Text { text: "' + content + '"; color: "' + secondaryTextColor + '"; wrapMode: Text.WordWrap; Layout.fillWidth: true; Layout.fillHeight: true; padding: Qt.rect(20, 0, 20, 0); } Button { text: "确定"; Layout.alignment: Qt.AlignRight; onClicked: messageBox.destroy(); } } }', mainWindow)
            }
            
            // 监听资源更新信号，更新资源管理窗口中的列表
            function onResourcesUpdated() {
                resourceWindow.updateResourceList();
            }
        }
        
        // 文件选择对话框
        Dialog {
            id: fileDialog
            title: "选择要导入的资源文件"
            visible: false
            standardButtons: Dialog.Ok | Dialog.Cancel
            
            onAccepted: {
                // 使用后端方法打开文件选择对话框
                backend.openFileDialog();
            }
        }
        
        // 资源管理窗口
    Window {
        id: resourceWindow
        title: "资源管理"
        width: 650
        height: 500
        visible: false
        modality: Qt.WindowModal
        flags: Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint
        color: mainWindow.backgroundColor
        
        property ListModel resourceModel: ListModel {}
        
        function updateResourceList() {
            // 清空现有数据
            resourceModel.clear();
            
            // 从后端获取资源列表
            var resources = backend.getResourceList();
            for (var i = 0; i < resources.length; i++) {
                var resource = resources[i];
                // 格式化文件大小
                var sizeStr = formatFileSize(resource.size);
                // 格式化修改时间
                var date = new Date(resource.modified * 1000);
                var dateStr = date.toLocaleString();
                
                resourceModel.append({
                    name: resource.name,
                    size: sizeStr,
                    modified: dateStr,
                    filePath: resource.path
                });
            }
        }
        
        function formatFileSize(bytes) {
            if (bytes < 1024) return bytes + ' B';
            else if (bytes < 1048576) return (bytes / 1024).toFixed(2) + ' KB';
            else return (bytes / 1048576).toFixed(2) + ' MB';
        }
        
        // 资源文件模型
        ListModel {
            id: resourceModel
        }
        
        ColumnLayout {
            anchors.fill: parent
            spacing: 10
            
            // 标题和操作按钮
            RowLayout {
                Layout.fillWidth: true
                spacing: 10
                
                Text {
                    text: "导入的资源文件"
                    font.pointSize: 16
                    font.bold: true
                    color: mainWindow.textPrimaryColor
                }
                
                Item { Layout.fillWidth: true }
                
                Button {
                    text: "选择文件"
                    onClicked: {
                        // 直接调用后端方法打开文件选择对话框
                        backend.openFileDialog();
                    }
                }
                
                Button {
                    text: "打开文件夹"
                    onClicked: {
                        backend.openResourceFolder();
                    }
                }
            }
            
            // 拖放区域
            Rectangle {
                id: dropArea
                Layout.fillWidth: true
                Layout.preferredHeight: 80
                color: mainWindow.surfaceColor
                border.color: mainWindow.borderColor
                border.width: 2
                radius: mainWindow.currentTheme.radius
                
                ColumnLayout {
            anchors.centerIn: parent
            spacing: 5

            Text {
                text: "拖放文件到此处导入"
                color: mainWindow.textPrimaryColor
                font.pointSize: 14
            }

            Text {
                text: "或点击上方'选择文件'按钮"
                color: mainWindow.textSecondaryColor
                font.pointSize: 12
            }
        }
                
                // 拖放功能
                MouseArea {
                    anchors.fill: parent
                    property bool dragOver: false

                    onEntered: {
                        dropArea.border.color = mainWindow.primaryColor;
                    }

                    onExited: {
                        dropArea.border.color = mainWindow.borderColor;
                    }

                    // 拖放功能通过系统API实现，此处保留UI反馈
                }
            }
            
            // 资源列表 - 使用ListView替代TableView
            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: mainWindow.surfaceColor
                border.color: mainWindow.borderColor
                radius: mainWindow.currentTheme.radius
                
                ColumnLayout {
                    anchors.fill: parent
                    spacing: 0
                    
                    // 表头
                    Rectangle {
                        Layout.fillWidth: true
                        height: 35
                        color: mainWindow.backgroundColor
                        RowLayout {
                            anchors.fill: parent
                            spacing: 0
                            
                            Text {
                            text: "文件名"
                            Layout.preferredWidth: 250
                            Layout.leftMargin: 5
                            Layout.topMargin: 5
                            font.bold: true
                            color: mainWindow.textPrimaryColor
                        }
                            
                            Text {
                            text: "大小"
                            Layout.preferredWidth: 100
                            Layout.leftMargin: 5
                            Layout.topMargin: 5
                            font.bold: true
                            color: mainWindow.textPrimaryColor
                            horizontalAlignment: Text.AlignHCenter
                        }
                            
                            Text {
                            text: "修改时间"
                            Layout.preferredWidth: 200
                            Layout.leftMargin: 5
                            Layout.topMargin: 5
                            font.bold: true
                            color: mainWindow.textPrimaryColor
                        }
                            
                            Text {
                            text: "操作"
                            Layout.preferredWidth: 80
                            Layout.leftMargin: 5
                            Layout.topMargin: 5
                            font.bold: true
                            color: mainWindow.textPrimaryColor
                            horizontalAlignment: Text.AlignHCenter
                        }
                        }
                    }
                    
                    // 列表内容
                    ScrollView {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        
                        ListView {
                            id: resourceList
                            anchors.fill: parent
                            model: resourceModel
                            delegate: Rectangle {
                                width: parent.width
                                height: 40
                                border.width: 1
                                
                                RowLayout {
                                    anchors.fill: parent
                                    spacing: 0
                                    
                                    Text {
                                        text: name
                                        Layout.preferredWidth: 250
                                        Layout.leftMargin: 5
                                        Layout.topMargin: 5
                                        color: mainWindow.textPrimaryColor
                                        elide: Text.ElideRight
                                    }
                                    
                                    Text {
                                        text: size
                                        Layout.preferredWidth: 100
                                        Layout.leftMargin: 5
                                        Layout.topMargin: 5
                                        color: mainWindow.textPrimaryColor
                                        horizontalAlignment: Text.AlignHCenter
                                    }
                                    
                                    Text {
                                        text: modified
                                        Layout.preferredWidth: 200
                                        Layout.leftMargin: 5
                                        Layout.topMargin: 5
                                        color: mainWindow.textPrimaryColor
                                        elide: Text.ElideRight
                                    }
                                    
                                    Button {
                                        text: "删除"
                                        Layout.preferredWidth: 80
                                        onClicked: {
                                            if (confirm("确定要删除这个文件吗？")) {
                                                backend.deleteResource(model.name);
                                            }
                                        }
                                    }
                                }
                                
                                MouseArea {
                                    anchors.fill: parent
                                    onEntered: parent.color = mainWindow.isDarkMode ? "#333333" : "#f9f9f9"
                                    onExited: parent.color = mainWindow.surfaceColor
                                }
                            }
                        }
                    }
                }
                
                // 空状态提示
                Rectangle {
                    anchors.fill: parent
                    visible: resourceModel.count === 0
                    color: "transparent"
                    
                    Text {
                    anchors.centerIn: parent
                    text: "暂无导入的资源文件"
                    color: mainWindow.textSecondaryColor
                }
                }
            }
        }
    }
        
        // 辅助函数：确认对话框
    function confirm(message) {
        // 简化的确认对话框实现
        return window.confirm(message);
    }
    }
}