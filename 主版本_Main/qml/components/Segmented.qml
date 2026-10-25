import QtQuick
import QtQuick.Controls

Item {
    id: root

    property var labels: []
    property int currentIndex: 0
    property color accentColor: "#4da6ff"
    property color baseColor: Qt.rgba(0.02, 0.035, 0.06, 0.32)
    property color borderColor: Qt.rgba(1, 1, 1, 0.11)
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
        color: Qt.rgba(0.30, 0.65, 1.0, 0.32)
        border.width: 1
        border.color: Qt.rgba(0.6, 0.85, 1.0, 0.45)
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
                    color: index === root.currentIndex ? "#f4f9ff" : "#8b9bb4"
                    font.family: "Microsoft YaHei UI"
                    font.pixelSize: 14
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
