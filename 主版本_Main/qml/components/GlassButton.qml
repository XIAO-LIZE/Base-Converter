import QtQuick
import QtQuick.Controls

Rectangle {
    id: root

    property string text: ""
    property int fontSize: 13
    property bool primary: false
    property color accentColor: "#4da6ff"
    signal clicked()

    implicitWidth: label.implicitWidth + 26
    implicitHeight: 34
    radius: 10
    color: primary ? Qt.rgba(0.30, 0.65, 1.0, 0.30)
                   : (mouse.containsMouse ? Qt.rgba(1, 1, 1, 0.10)
                                          : Qt.rgba(1, 1, 1, 0.05))
    border.width: 1
    border.color: primary ? Qt.rgba(0.60, 0.85, 1.0, 0.45)
                          : Qt.rgba(1, 1, 1, 0.13)

    Behavior on color { ColorAnimation { duration: 120 } }

    Text {
        id: label
        anchors.centerIn: parent
        text: root.text
        color: root.primary ? "#f4f9ff" : "#9fb0c8"
        font.family: "Microsoft YaHei UI"
        font.pixelSize: root.fontSize
        font.bold: root.primary
    }

    MouseArea {
        id: mouse
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        onClicked: root.clicked()
    }
}
