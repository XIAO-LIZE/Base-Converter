import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects
import "components"
import "pages"

Window {
    id: root

    width: 1180
    height: 940
    minimumWidth: 980
    minimumHeight: 820
    visible: true
    color: "#05080e"
    title: "BaseConverter"
    flags: Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint

    property int tab: 0
    property var s: backend.strings
    readonly property bool maximized: visibility === Window.Maximized

    // ---- background -------------------------------------------------
    Item {
        id: bgRoot
        anchors.fill: parent

        Rectangle {
            anchors.fill: parent
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#04070d" }
                GradientStop { position: 0.55; color: "#071120" }
                GradientStop { position: 1.0; color: "#0a1828" }
            }
        }

        RadialGradient {
            anchors.fill: parent
            horizontalOffset: 330
            verticalOffset: -330
            horizontalRadius: 680
            verticalRadius: 680
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#662563eb" }
                GradientStop { position: 0.55; color: "#242563eb" }
                GradientStop { position: 1.0; color: "#002563eb" }
            }
        }

        RadialGradient {
            anchors.fill: parent
            horizontalOffset: -440
            verticalOffset: 210
            horizontalRadius: 500
            verticalRadius: 500
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#380ea5e9" }
                GradientStop { position: 0.6; color: "#140ea5e9" }
                GradientStop { position: 1.0; color: "#000ea5e9" }
            }
        }

        RadialGradient {
            anchors.fill: parent
            horizontalOffset: 430
            verticalOffset: 390
            horizontalRadius: 460
            verticalRadius: 460
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#407c3aed" }
                GradientStop { position: 0.6; color: "#167c3aed" }
                GradientStop { position: 1.0; color: "#007c3aed" }
            }
        }

        RadialGradient {
            anchors.fill: parent
            horizontalOffset: 10
            verticalOffset: 40
            horizontalRadius: 420
            verticalRadius: 380
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#1c22d3ee" }
                GradientStop { position: 0.55; color: "#0c22d3ee" }
                GradientStop { position: 1.0; color: "#0022d3ee" }
            }
        }
    }

    // ---- custom title bar (frameless window) -----------------------
    Item {
        id: titleBar
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        height: 38
        z: 5

        MouseArea {
            anchors.fill: parent
            onPressed: root.startSystemMove()
            onDoubleClicked: root.maximized ? root.showNormal() : root.showMaximized()
        }

        Row {
            anchors.left: parent.left
            anchors.leftMargin: 16
            anchors.verticalCenter: parent.verticalCenter
            spacing: 9

            Rectangle {
                width: 18; height: 18; radius: 5
                color: "transparent"
                clip: true
                Image {
                    anchors.fill: parent
                    source: "../icon.png"
                    fillMode: Image.PreserveAspectFit
                    smooth: true
                }
            }

            Text {
                anchors.verticalCenter: parent.verticalCenter
                text: root.s.appTitle
                color: "#65778f"
                font.family: "Microsoft YaHei UI"
                font.pixelSize: 11
            }
        }

        Row {
            anchors.right: parent.right
            anchors.rightMargin: 8
            anchors.top: parent.top
            anchors.topMargin: 4
            spacing: 2
            z: 6

            Rectangle {
                width: 40; height: 30; radius: 8
                color: minMouse.containsMouse ? Qt.rgba(1, 1, 1, 0.08) : "transparent"
                Text {
                    anchors.centerIn: parent
                    text: "—"
                    color: "#93a4bd"
                    font.family: "Segoe UI"
                    font.pixelSize: 13
                }
                MouseArea {
                    id: minMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.showMinimized()
                }
            }

            Rectangle {
                width: 40; height: 30; radius: 8
                color: maxMouse.containsMouse ? Qt.rgba(1, 1, 1, 0.08) : "transparent"
                Text {
                    anchors.centerIn: parent
                    text: root.maximized ? "❐" : "□"
                    color: "#93a4bd"
                    font.family: "Segoe UI"
                    font.pixelSize: 12
                }
                MouseArea {
                    id: maxMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.maximized ? root.showNormal() : root.showMaximized()
                }
            }

            Rectangle {
                width: 40; height: 30; radius: 8
                color: closeMouse.containsMouse ? "#e81123" : "transparent"
                Text {
                    anchors.centerIn: parent
                    text: "✕"
                    color: closeMouse.containsMouse ? "#ffffff" : "#93a4bd"
                    font.family: "Segoe UI"
                    font.pixelSize: 12
                }
                MouseArea {
                    id: closeMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: Qt.quit()
                }
            }
        }
    }

    // Edge/corner resize handles for the frameless window.
    MouseArea {
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        width: 5
        z: 7
        enabled: !root.maximized
        cursorShape: Qt.SizeHorCursor
        onPressed: root.startSystemResize(Qt.LeftEdge)
    }
    MouseArea {
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        width: 5
        z: 7
        enabled: !root.maximized
        cursorShape: Qt.SizeHorCursor
        onPressed: root.startSystemResize(Qt.RightEdge)
    }
    MouseArea {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        height: 5
        z: 7
        enabled: !root.maximized
        cursorShape: Qt.SizeVerCursor
        onPressed: root.startSystemResize(Qt.TopEdge)
    }
    MouseArea {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        height: 5
        z: 7
        enabled: !root.maximized
        cursorShape: Qt.SizeVerCursor
        onPressed: root.startSystemResize(Qt.BottomEdge)
    }
    MouseArea {
        anchors.left: parent.left
        anchors.top: parent.top
        width: 10
        height: 10
        z: 8
        enabled: !root.maximized
        cursorShape: Qt.SizeFDiagCursor
        onPressed: root.startSystemResize(Qt.LeftEdge | Qt.TopEdge)
    }
    MouseArea {
        anchors.right: parent.right
        anchors.top: parent.top
        width: 10
        height: 10
        z: 8
        enabled: !root.maximized
        cursorShape: Qt.SizeBDiagCursor
        onPressed: root.startSystemResize(Qt.RightEdge | Qt.TopEdge)
    }
    MouseArea {
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        width: 10
        height: 10
        z: 8
        enabled: !root.maximized
        cursorShape: Qt.SizeBDiagCursor
        onPressed: root.startSystemResize(Qt.LeftEdge | Qt.BottomEdge)
    }
    MouseArea {
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        width: 10
        height: 10
        z: 8
        enabled: !root.maximized
        cursorShape: Qt.SizeFDiagCursor
        onPressed: root.startSystemResize(Qt.RightEdge | Qt.BottomEdge)
    }

    // ---- header -----------------------------------------------------
    Item {
        id: header
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.leftMargin: 44
        anchors.rightMargin: 44
        anchors.topMargin: 50
        height: 84


        Image {
            id: logo
            width: 46; height: 46
            source: "../icon.png"
            fillMode: Image.PreserveAspectFit
            smooth: true
        }

        Text {
            anchors.left: logo.right
            anchors.leftMargin: 16
            anchors.top: logo.top
            anchors.topMargin: -2
            text: root.s.appTitle
            color: "#f2f7ff"
            font.family: "Microsoft YaHei UI"
            font.pixelSize: 28
            font.bold: true
        }

        Text {
            anchors.left: logo.right
            anchors.leftMargin: 16
            anchors.top: logo.top
            anchors.topMargin: 38
            text: root.s.appSub
            color: "#8496ad"
            font.family: "Microsoft YaHei UI"
            font.pixelSize: 12
        }

        Rectangle {
            id: langButton
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.topMargin: 6
            width: 64
            height: 34
            radius: 10
            z: 10
            color: langButtonMouse.containsMouse ? Qt.rgba(1, 1, 1, 0.10)
                                                 : Qt.rgba(1, 1, 1, 0.05)
            border.width: 1
            border.color: Qt.rgba(1, 1, 1, 0.13)

            Text {
                anchors.centerIn: parent
                text: backend.lang === "zh" ? "EN" : "中"
                color: "#9fb0c8"
                font.family: "Microsoft YaHei UI"
                font.pixelSize: 13
            }
        }

        MouseArea {
            id: langButtonMouse
            x: parent.width - 64
            y: 6
            width: 64
            height: 34
            z: 40
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            onClicked: backend.toggleLang()
        }
    }

    // ---- tab bar ----------------------------------------------------
    GlassCard {
        id: tabBar
        backdrop: bgRoot
        x: 44
        y: 150
        width: 500
        height: 58
        radius: 18
        padding: 6
        tint: Qt.rgba(0.04, 0.065, 0.10, 0.55)

        readonly property real gap: 6
        readonly property int count: root.s.tabs.length
        readonly property real itemWidth: count > 0
            ? (tabBar.contentItem.width - gap * (count - 1)) / count : 0

        Rectangle {
            id: tabSelection
            y: 0
            height: tabBar.contentItem.height
            width: tabBar.itemWidth
            x: root.tab * (tabBar.itemWidth + tabBar.gap)
            radius: 13
            color: Qt.rgba(0.30, 0.65, 1.0, 0.28)
            border.width: 1
            border.color: Qt.rgba(0.60, 0.85, 1.0, 0.42)
            Behavior on x { NumberAnimation { duration: 220; easing.type: Easing.OutCubic } }
        }

        Row {
            anchors.fill: parent
            spacing: tabBar.gap
            Repeater {
                model: tabBar.count
                delegate: Item {
                    width: tabBar.itemWidth
                    height: parent ? parent.height : 0
                    Text {
                        anchors.centerIn: parent
                        text: root.s.tabs[index]
                        color: index === root.tab ? "#f4f9ff" : "#8496ad"
                        font.family: "Microsoft YaHei UI"
                        font.pixelSize: 14
                        font.bold: index === root.tab
                        Behavior on color { ColorAnimation { duration: 160 } }
                    }
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: root.tab = index
                    }
                }
            }
        }
    }

    // ---- pages ------------------------------------------------------
    StackLayout {
        id: pages
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: footer.top
        anchors.leftMargin: 44
        anchors.rightMargin: 44
        anchors.topMargin: 220
        anchors.bottomMargin: 14
        currentIndex: root.tab

        ConverterPage { backdrop: bgRoot }
        AsciiPage { backdrop: bgRoot }
        Ipv4Page { backdrop: bgRoot }
    }

    // ---- footer -----------------------------------------------------
    GlassCard {
        id: footer
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.leftMargin: 44
        anchors.rightMargin: 44
        anchors.bottomMargin: 16
        height: 46
        radius: 20
        padding: 10
        tint: Qt.rgba(0.035, 0.055, 0.085, 0.55)

        Text {
            anchors.left: parent.left
            anchors.leftMargin: 8
            anchors.verticalCenter: parent.verticalCenter
            text: backend.statusText
            color: "#7f91aa"
            font.family: "Microsoft YaHei UI"
            font.pixelSize: 11
        }

        Text {
            anchors.right: parent.right
            anchors.rightMargin: 8
            anchors.verticalCenter: parent.verticalCenter
            text: root.s.version
            color: "#7f91aa"
            font.family: "Microsoft YaHei UI"
            font.pixelSize: 11
        }
    }

    Component.onCompleted: {
        backend.convert("", 2)
        backend.searchAscii("")
        backend.parseIp("")
    }

    Shortcut {
        sequence: "Ctrl+L"
        onActivated: backend.toggleLang()
    }
}
