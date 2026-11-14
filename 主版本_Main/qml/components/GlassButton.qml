import QtQuick
import QtQuick.Controls

Rectangle {
    id: root

    property string text: ""
    property int fontSize: 13
    property bool primary: false
    property color accentColor: theme.colors.accent
    signal clicked()

    implicitWidth: label.implicitWidth + 26
    implicitHeight: 34
    radius: 10
    color: primary ? theme.colors.primaryTint
                   : (mouse.containsMouse ? theme.colors.buttonHover
                                          : theme.colors.buttonTint)
    border.width: 1
    border.color: primary ? theme.colors.primaryBorder
                          : theme.colors.buttonBorder

    Behavior on color { ColorAnimation { duration: 120 } }

    Text {
        id: label
        anchors.centerIn: parent
        text: root.text
        color: root.primary ? theme.colors.primaryText : theme.colors.buttonText
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
