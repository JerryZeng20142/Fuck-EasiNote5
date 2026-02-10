import QtQuick 2.15
import QtQuick.Controls 2.15
import RinUI 1.0

Rectangle {
    width: 400
    height: 300
    color: Theme.backgroundColor
    
    Column {
        anchors.centerIn: parent
        spacing: 20
        
        Text {
            text: "RinUI集成测试"
            font.pixelSize: 24
            font.bold: true
            color: Theme.accentColor
            horizontalAlignment: Text.AlignHCenter
        }
        
        Button {
            text: "点击测试"
            onClicked: {
                console.log("RinUI按钮点击成功！")
            }
            width: 200
        }
        
        CheckBox {
            text: "测试复选框"
            checked: true
        }
        
        Switch {
            text: "测试开关"
            checked: false
        }
    }
}