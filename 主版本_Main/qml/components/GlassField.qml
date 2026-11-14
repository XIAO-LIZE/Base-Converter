import QtQuick
import QtQuick.Controls

Item {
    id: root

    property alias text: field.text
    property string placeholder: ""
    property int fontSize: 17
    property bool monospace: false
    property bool showClear: true
    property color fieldColor: theme.colors.fieldTint
    property color borderColor: theme.colors.fieldBorder
    property color focusColor: theme.colors.accent
    property alias readOnly: field.readOnly

    signal edited()
    signal accepted()

    implicitHeight: 48

    Rectangle {
        anchors.fill: parent
        radius: 12
        color: root.fieldColor
        border.width: field.activeFocus ? 2 : 1
        border.color: field.activeFocus ? root.focusColor : root.borderColor
    }

    TextField {
        id: field
        anchors.fill: parent
        anchors.leftMargin: 15
        anchors.rightMargin: root.showClear && field.text.length > 0 ? 42 : 15
        background: null
        color: theme.colors.fieldText
        placeholderText: root.placeholder
        placeholderTextColor: theme.colors.placeholder
        font.family: root.monospace ? "Consolas" : "Microsoft YaHei UI"
        font.pixelSize: root.fontSize
        verticalAlignment: TextInput.AlignVCenter
        selectByMouse: true
        onTextChanged: root.edited()
        onAccepted: root.accepted()

        Keys.onEscapePressed: {
            field.text = ""
            root.edited()
        }
    }

    Rectangle {
        visible: root.showClear && field.text.length > 0
        width: 26
        height: 26
        radius: 7
        anchors.right: parent.right
        anchors.rightMargin: 9
        anchors.verticalCenter: parent.verticalCenter
        color: clearMouse.containsMouse ? theme.colors.clearHover
                                        : theme.colors.clearTint
        Text {
            anchors.centerIn: parent
            text: "×"
            color: theme.colors.clearText
            font.pixelSize: 19
            font.family: "Segoe UI"
        }
        MouseArea {
            id: clearMouse
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            onClicked: {
                field.text = ""
                root.edited()
                field.forceActiveFocus()
            }
        }
    }
}
