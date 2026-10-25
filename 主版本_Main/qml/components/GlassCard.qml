import QtQuick
import QtQuick.Effects
import Qt5Compat.GraphicalEffects

Item {
    id: root

    property Item backdrop: null
    property real radius: 22
    property real padding: 18
    property color tint: Qt.rgba(0.055, 0.085, 0.13, 0.18)
    property color edge: Qt.rgba(0.78, 0.86, 1.0, 0.16)
    property bool blur: true

    default property alias contentData: content.data
    property alias contentItem: content

    // Soft drop shadow behind the glass panel.
    Rectangle {
        id: shadowShape
        anchors.fill: parent
        anchors.topMargin: 0
        radius: root.radius
        color: "#000000"
        visible: false
    }
    DropShadow {
        anchors.fill: shadowShape
        source: shadowShape
        radius: 28
        samples: 25
        color: "#000000"
        opacity: 0.45
        verticalOffset: 10
    }

    // Backdrop blur: capture the background region underneath this panel.
    ShaderEffectSource {
        id: snap
        sourceItem: root.backdrop
        sourceRect: {
            // Reference the geometry so the capture follows layout changes.
            var guard = root.x + root.y + root.width + root.height
            var p = root.backdrop ? root.mapToItem(root.backdrop, 0, 0)
                                  : Qt.point(0, 0)
            return Qt.rect(p.x, p.y, root.width, root.height)
        }
        live: true
        hideSource: false
        visible: false
    }

    GaussianBlur {
        id: blurFx
        anchors.fill: parent
        source: snap
        radius: 48
        samples: 25
        visible: false
    }

    Rectangle {
        id: maskShape
        anchors.fill: parent
        radius: root.radius
        color: "#ffffff"
        visible: false
    }

    OpacityMask {
        anchors.fill: parent
        source: blurFx
        maskSource: maskShape
        visible: root.blur
    }

    Rectangle {
        anchors.fill: parent
        radius: root.radius
        color: root.tint
        border.width: 1
        border.color: root.edge
    }

    // Specular highlight along the top edge.
    Rectangle {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.leftMargin: root.radius
        anchors.rightMargin: root.radius
        height: 1
        color: Qt.rgba(1, 1, 1, 0.28)
    }

    Item {
        id: content
        anchors.fill: parent
        anchors.margins: root.padding
    }
}
