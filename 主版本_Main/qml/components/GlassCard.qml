import QtQuick
import Qt5Compat.GraphicalEffects

Item {
    id: root

    property Item backdrop: null
    property real radius: 22
    property real padding: 18
    property color tint: theme.colors.cardTint
    property color edge: theme.colors.cardEdge
    property color specular: theme.colors.cardHighlight

    // Optical parameters. Refraction is in pixels; aberration is a fraction.
    property real refraction: 12
    property real aberration: 0.018
    property real blurRadius: 22
    property bool glassReady: false

    default property alias contentData: content.data
    property alias contentItem: content

    HoverHandler {
        id: hover
    }

    // Soft ambient shadow behind the glass panel. Use a border ring rather
    // than a filled rectangle so the shadow cannot darken the glass itself.
    Rectangle {
        id: shadowShape
        anchors.fill: parent
        radius: root.radius
        color: "transparent"
        border.width: 2
        border.color: theme.colors.shadow
        visible: false
    }
    DropShadow {
        anchors.fill: shadowShape
        source: shadowShape
        radius: 30
        samples: 27
        color: theme.colors.shadow
        opacity: theme.colors.shadowOpacity
        verticalOffset: 12
    }

    // Capture the scene underneath the panel, then soften it before lensing.
    ShaderEffectSource {
        id: snap
        sourceItem: root.backdrop
        sourceRect: {
            // Reference the geometry so the capture follows layout changes.
            var guard = root.x + root.y + root.width + root.height
            if (root.backdrop)
                guard += root.backdrop.width + root.backdrop.height
            var p = root.backdrop ? root.mapToItem(root.backdrop, 0, 0)
                                  : Qt.point(0, 0)
            return Qt.rect(p.x, p.y, root.width, root.height)
        }
        live: true
        hideSource: false
        visible: false
    }

    Timer {
        interval: 300
        running: true
        repeat: false
        onTriggered: {
            if (root.backdrop && root.width > 0) {
                snap.sourceItem = null
                snap.sourceItem = root.backdrop
                root.glassReady = true
            }
        }
    }

    Rectangle {
        anchors.fill: parent
        radius: root.radius
        color: root.tint
        visible: !root.glassReady
    }

    // The glass material: blurred backdrop, edge lensing and chromatic fringe.
    ShaderEffect {
        anchors.fill: parent
        property var source: snap
        property color tint: root.tint
        property vector2d surfaceSize: Qt.vector2d(width, height)
        property real radius: root.radius
        property real refraction: root.refraction
        property real aberration: root.aberration
        property real blurRadius: root.blurRadius
        fragmentShader: "../shaders/glass.frag.qsb"
        opacity: root.glassReady ? 1 : 0
    }

    // A crisp rim and a small specular streak keep the glass edge legible.
    Rectangle {
        anchors.fill: parent
        radius: root.radius
        color: "transparent"
        border.width: 1
        border.color: root.edge
    }

    Rectangle {
        x: root.radius * 0.7
        y: 1
        width: Math.max(0, root.width - root.radius * 1.4)
        height: 1.5
        radius: 1
        color: root.specular
        opacity: hover.hovered ? 0.72 : 0.52
    }
    Item {
        id: content
        anchors.fill: parent
        anchors.margins: root.padding
    }
}
