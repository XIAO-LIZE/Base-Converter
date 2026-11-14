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
    x: Screen.width > 0 ? Math.max(0, Math.round((Screen.width - width) / 2)) : 0
    y: Screen.height > 0 ? Math.max(0, Math.round((Screen.height - height) / 2)) : 0
    visible: true
    color: theme.colors.window
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
                GradientStop { position: 0.0; color: theme.colors.bgTop }
                GradientStop { position: 0.55; color: theme.colors.bgMid }
                GradientStop { position: 1.0; color: theme.colors.bgBottom }
            }
        }

        RadialGradient {
            anchors.fill: parent
            horizontalOffset: 330
            verticalOffset: -330
            horizontalRadius: 680
            verticalRadius: 680
            gradient: Gradient {
                GradientStop { position: 0.0; color: theme.colors.glow1 }
                GradientStop { position: 0.55; color: theme.colors.glow2 }
                GradientStop { position: 1.0; color: theme.colors.glow3 }
            }
        }

        RadialGradient {
            anchors.fill: parent
            horizontalOffset: -440
            verticalOffset: 210
            horizontalRadius: 500
            verticalRadius: 500
            gradient: Gradient {
                GradientStop { position: 0.0; color: theme.colors.glow4 }
                GradientStop { position: 0.6; color: theme.colors.glow5 }
                GradientStop { position: 1.0; color: theme.colors.glow6 }
            }
        }

        RadialGradient {
            anchors.fill: parent
            horizontalOffset: 430
            verticalOffset: 390
            horizontalRadius: 460
            verticalRadius: 460
            gradient: Gradient {
                GradientStop { position: 0.0; color: theme.colors.glow7 }
                GradientStop { position: 0.6; color: theme.colors.glow8 }
                GradientStop { position: 1.0; color: theme.colors.glow9 }
            }
        }

        RadialGradient {
            anchors.fill: parent
            horizontalOffset: 10
            verticalOffset: 40
            horizontalRadius: 420
            verticalRadius: 380
            gradient: Gradient {
                GradientStop { position: 0.0; color: theme.colors.glow10 }
                GradientStop { position: 0.55; color: theme.colors.glow11 }
                GradientStop { position: 1.0; color: theme.colors.glow12 }
            }
        }

        // Broad colour fields and grain give the glass something to refract.
        RadialGradient {
            width: parent.width * 0.50
            height: width
            x: parent.width * 0.50
            y: parent.height * 0.02
            horizontalOffset: width * 0.5
            verticalOffset: height * 0.5
            horizontalRadius: width * 0.5
            verticalRadius: height * 0.5
            gradient: Gradient {
                GradientStop { position: 0.0; color: theme.colors.decor1 }
                GradientStop { position: 0.62; color: theme.colors.decor1 }
                GradientStop { position: 1.0; color: "#00000000" }
            }
        }

        RadialGradient {
            width: parent.width * 0.46
            height: width
            x: -parent.width * 0.15
            y: parent.height * 0.58
            horizontalOffset: width * 0.5
            verticalOffset: height * 0.5
            horizontalRadius: width * 0.5
            verticalRadius: height * 0.5
            gradient: Gradient {
                GradientStop { position: 0.0; color: theme.colors.decor2 }
                GradientStop { position: 0.60; color: theme.colors.decor2 }
                GradientStop { position: 1.0; color: "#00000000" }
            }
        }

        Repeater {
            model: 4
            Rectangle {
                width: 1
                height: parent.height * 1.45
                x: parent.width * (0.14 + index * 0.19)
                y: -parent.height * 0.20
                rotation: -18
                color: theme.colors.decorLine
            }
        }

        Image {
            anchors.fill: parent
            source: "assets/noise.png"
            fillMode: Image.Tile
            smooth: false
            opacity: theme.colors.noiseOpacity
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
                color: theme.colors.textDim
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
                color: minMouse.containsMouse ? theme.colors.controlHover : "transparent"
                Rectangle {
                    anchors.centerIn: parent
                    width: 10; height: 1
                    color: minMouse.containsMouse ? theme.colors.iconActive : theme.colors.icon
                    antialiasing: true
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
                color: maxMouse.containsMouse ? theme.colors.controlHover : "transparent"
                Item {
                    anchors.centerIn: parent
                    width: 14; height: 14

                    Rectangle {
                        anchors.centerIn: parent
                        visible: !root.maximized
                        width: 10; height: 10
                        color: "transparent"
                        border.width: 1
                        border.color: maxMouse.containsMouse ? theme.colors.iconActive : theme.colors.icon
                        radius: 1
                        antialiasing: true
                    }

                    Item {
                        anchors.centerIn: parent
                        visible: root.maximized
                        width: 12; height: 12

                        Rectangle {
                            x: 2; y: 0
                            width: 9; height: 9
                            color: "transparent"
                            border.width: 1
                            border.color: maxMouse.containsMouse ? theme.colors.iconActive : theme.colors.icon
                            radius: 1
                            antialiasing: true
                        }
                        Rectangle {
                            x: 0; y: 2
                            width: 9; height: 9
                            color: "transparent"
                            border.width: 1
                            border.color: maxMouse.containsMouse ? theme.colors.iconActive : theme.colors.icon
                            radius: 1
                            antialiasing: true
                        }
                    }
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
                color: closeMouse.containsMouse ? theme.colors.closeHover : "transparent"
                Item {
                    anchors.centerIn: parent
                    width: 12; height: 12

                    Rectangle {
                        anchors.centerIn: parent
                        width: 11; height: 1
                        color: closeMouse.containsMouse ? theme.colors.onClose : theme.colors.icon
                        rotation: 45
                        antialiasing: true
                    }
                    Rectangle {
                        anchors.centerIn: parent
                        width: 11; height: 1
                        color: closeMouse.containsMouse ? theme.colors.onClose : theme.colors.icon
                        rotation: -45
                        antialiasing: true
                    }
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
            color: theme.colors.text
            font.family: "Microsoft YaHei UI"
            font.pixelSize: 28
            font.weight: Font.Bold
            font.letterSpacing: 0.2
        }

        Text {
            anchors.left: logo.right
            anchors.leftMargin: 16
            anchors.top: logo.top
            anchors.topMargin: 38
            text: root.s.appSub
            color: theme.colors.textSecondary
            font.family: "Microsoft YaHei UI"
            font.pixelSize: 12
            font.letterSpacing: 0.25
        }

        Row {
            id: headerControls
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.topMargin: 6
            spacing: 8
            z: 10

            GlassSegmented {
                id: themeSwitch
                width: 222
                height: 34
                fontSize: 11
                labels: [root.s.themeDark, root.s.themeLight, root.s.themeSystem]
                currentIndex: theme.mode === "dark" ? 0
                            : theme.mode === "light" ? 1 : 2
                onActivated: function (index) {
                    theme.setMode(["dark", "light", "system"][index])
                }
            }

            GlassSegmented {
                id: langSwitch
                width: 100
                height: 34
                fontSize: 11
                labels: ["中文", "EN"]
                currentIndex: backend.lang === "zh" ? 0 : 1
                onActivated: function (index) {
                    if (index !== (backend.lang === "zh" ? 0 : 1))
                        backend.toggleLang()
                }
            }
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
        tint: theme.colors.tabBarTint

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
            color: theme.colors.tabSelection
            border.width: 1
            border.color: theme.colors.tabSelectionBorder
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
                        color: index === root.tab ? theme.colors.tabTextActive : theme.colors.textSecondary
                        font.family: "Microsoft YaHei UI"
                        font.pixelSize: 14
                        font.weight: index === root.tab ? Font.DemiBold : Font.Normal
                        font.letterSpacing: 0.2
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
        height: 50
        radius: 18
        padding: 12
        tint: theme.colors.footerTint

        Row {
            id: statusGroup
            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter
            spacing: 9

            Item {
                width: 12
                height: 12
                anchors.verticalCenter: parent.verticalCenter

                Rectangle {
                    anchors.fill: parent
                    radius: width / 2
                    color: backend.statusText === root.s.copied
                           ? theme.colors.accent : theme.colors.success
                    opacity: 0.16
                }
                Rectangle {
                    width: 6
                    height: 6
                    radius: width / 2
                    anchors.centerIn: parent
                    color: backend.statusText === root.s.copied
                           ? theme.colors.accent : theme.colors.success
                }
            }

            Text {
                anchors.verticalCenter: parent.verticalCenter
                text: backend.statusText
                color: theme.colors.textSecondary
                font.family: "Microsoft YaHei UI"
                font.pixelSize: 12
                font.weight: Font.DemiBold
                font.letterSpacing: 0.2
            }
        }

        Row {
            id: runtimeGroup
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            spacing: 9

            Text {
                anchors.verticalCenter: parent.verticalCenter
                text: "v" + backend.appVersion
                color: theme.colors.textSecondary
                font.family: "Microsoft YaHei UI"
                font.pixelSize: 11
                font.weight: Font.DemiBold
                font.letterSpacing: 0.3
            }

            Rectangle {
                width: 1
                height: 12
                anchors.verticalCenter: parent.verticalCenter
                color: theme.colors.rowBorder
            }

            Text {
                anchors.verticalCenter: parent.verticalCenter
                text: root.s.version
                color: theme.colors.textMuted
                font.family: "Microsoft YaHei UI"
                font.pixelSize: 10
                font.letterSpacing: 0.4
            }
        }
    }

    // One-time startup overlay for the first packaged launch.
    Rectangle {
        id: startupOverlay
        anchors.fill: parent
        z: 200
        color: theme.colors.window
        opacity: 1
        visible: backend.packaged && backend.firstRun && opacity > 0

        Behavior on opacity {
            NumberAnimation { duration: 240; easing.type: Easing.OutCubic }
        }

        Column {
            anchors.centerIn: parent
            spacing: 16

            Image {
                width: 64; height: 64
                anchors.horizontalCenter: parent.horizontalCenter
                source: "../icon.png"
                fillMode: Image.PreserveAspectFit
                smooth: true
            }

            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                text: root.s.appTitle
                color: theme.colors.text
                font.family: "Microsoft YaHei UI"
                font.pixelSize: 26
                font.bold: true
            }

            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                text: root.s.loading
                color: theme.colors.textSecondary
                font.family: "Microsoft YaHei UI"
                font.pixelSize: 13
            }

            Rectangle {
                width: 220; height: 3; radius: 1.5
                anchors.horizontalCenter: parent.horizontalCenter
                color: theme.colors.tabSelection

                Rectangle {
                    height: parent.height
                    radius: 1.5
                    color: theme.colors.accent
                    NumberAnimation on width {
                        from: 0; to: 220
                        duration: 900
                        easing.type: Easing.InOutCubic
                        running: backend.packaged && backend.firstRun
                    }
                }
            }
        }

        Timer {
            interval: 1000
            running: backend.packaged && backend.firstRun
            onTriggered: {
                backend.markStarted()
                startupOverlay.opacity = 0
            }
        }
    }

    Component.onCompleted: {
        root.tab = 0
        backend.convert("", 0)
        backend.searchAscii("")
        backend.parseIp("")
    }

    Shortcut {
        sequence: "Ctrl+L"
        onActivated: backend.toggleLang()
    }
}
