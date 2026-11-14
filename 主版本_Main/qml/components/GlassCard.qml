import QtQuick
import QtQuick.Effects
import Qt5Compat.GraphicalEffects

Item {
    id: root

    property Item backdrop: null
    property real radius: 22
    property real padding: 18
    property color tint: theme.colors.cardTint
    property color edge: theme.colors.cardEdge
    property bool blur: true

    default property alias contentData: content.data
    property alias contentItem: content

    // Soft drop shadow behind the glass panel.
    Rectangle {
        id: shadowShape
        anchors.fill: parent
        anchors.topMargin: 0
        radius: root.radius
        color: theme.colors.shadow
        visible: false
    }
    DropShadow {
        anchors.fill: shadowShape
        source: shadowShape
        radius: 28
        samples: 25
        color: theme.colors.shadow
        opacity: theme.colors.shadowOpacity
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
        color: theme.colors.cardHighlight
    }

    Item {
        id: content
        anchors.fill: parent
        anchors.margins: root.padding
    }
}
