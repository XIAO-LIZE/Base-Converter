import QtQuick
import QtQuick.Controls

Item {
    id: root

    property var labels: []
    property int currentIndex: 0
    property int fontSize: 14
    property color accentColor: theme.colors.accent
    property color baseColor: theme.colors.segTint
    property color borderColor: theme.colors.segBorder
    signal activated(int index)

    implicitHeight: 40

    readonly property real inset: 3
    readonly property real gap: 8
    readonly property int count: labels.length
    readonly property real itemWidth: count > 0
        ? (width - 2 * inset - gap * (count - 1)) / count : 0

    Rectangle {
        anchors.fill: parent
        radius: 12
        color: root.baseColor
        border.width: 1
        border.color: root.borderColor
    }

    Rectangle {
        id: selection
        height: parent.height - 2 * root.inset
        width: root.itemWidth
        radius: 10
        y: root.inset
        x: root.inset + root.currentIndex * (root.itemWidth + root.gap)
        color: theme.colors.segSelection
        border.width: 1
        border.color: theme.colors.segSelectionBorder
        Behavior on x { NumberAnimation { duration: 180; easing.type: Easing.OutCubic } }
        Behavior on width { NumberAnimation { duration: 180; easing.type: Easing.OutCubic } }
    }

    Row {
        anchors.fill: parent
        anchors.margins: root.inset
        spacing: root.gap
        Repeater {
            model: root.count
            delegate: Item {
                width: root.itemWidth
                height: parent ? parent.height : 0
                Text {
                    anchors.centerIn: parent
                    text: root.labels[index] !== undefined ? root.labels[index] : ""
                    color: index === root.currentIndex ? theme.colors.segTextActive : theme.colors.segText
                    font.family: "Microsoft YaHei UI"
                    font.pixelSize: root.fontSize
                    font.bold: index === root.currentIndex
                    Behavior on color { ColorAnimation { duration: 150 } }
                }
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.activated(index)
                }
            }
        }
    }
}
