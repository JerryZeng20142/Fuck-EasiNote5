import QtQuick 2.15

// RinUI主组件 - 统一导入点
QtObject {
    id: rinu
    
    // 导出组件
    property Component Controls: Qt.createComponent("Controls.qml")
    property Component Theme: Qt.createComponent("Theme.qml")
    property Component TextField: Qt.createComponent("TextField.qml")
    property Component ComboBox: Qt.createComponent("ComboBox.qml")
    property Component Card: Qt.createComponent("Card.qml")
    
    // 组件加载状态检查
    Component.onCompleted: {
        // 确保所有组件都能正确加载
        if (Controls.status === Component.Error) {
            console.log("无法加载Controls组件:", Controls.errorString())
        }
        if (Theme.status === Component.Error) {
            console.log("无法加载Theme组件:", Theme.errorString())
        }
        if (TextField.status === Component.Error) {
            console.log("无法加载TextField组件:", TextField.errorString())
        }
        if (ComboBox.status === Component.Error) {
            console.log("无法加载ComboBox组件:", ComboBox.errorString())
        }
        if (Card.status === Component.Error) {
            console.log("无法加载Card组件:", Card.errorString())
        }
        
        console.log("RinUI组件加载完成")
    }
}