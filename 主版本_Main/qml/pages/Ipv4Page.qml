import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"

Item {
    id: page

    property Item backdrop
    property var s: backend.strings

    ColumnLayout {
        anchors.fill: parent
        spacing: 12

        GlassCard {
            backdrop: page.backdrop
            Layout.fillWidth: true
            Layout.preferredHeight: 166
            radius: 22

            ColumnLayout {
                anchors.fill: parent
                spacing: 10

                Text {
                    text: page.s.ipTitle
                    color: "#e8eef9"
                    font.family: "Microsoft YaHei UI"
                    font.pixelSize: 16
                    font.bold: true
                }

                GlassField {
                    id: ipField
                    Layout.fillWidth: true
                    Layout.preferredHeight: 48
                    placeholder: page.s.ipInput
                    monospace: true
                    fontSize: 18
                    onEdited: backend.parseIp(text)
                }

                Text {
                    Layout.fillWidth: true
                    text: backend.ipMessage
                    color: backend.ipError ? "#ef4444" : "#7f91aa"
                    font.family: "Microsoft YaHei UI"
                    font.pixelSize: 12
                    elide: Text.ElideRight
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 12

            GlassCard {
                backdrop: page.backdrop
                Layout.fillWidth: true
                Layout.fillHeight: true
                radius: 22

                ColumnLayout {
                    anchors.fill: parent
                    spacing: 6

                    Text {
                        text: page.s.addressRep
                        color: "#e8eef9"
                        font.family: "Microsoft YaHei UI"
                        font.pixelSize: 15
                        font.bold: true
                    }

                    Repeater {
                        model: backend.ipRows
                        delegate: Rectangle {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 40
                            radius: 9
                            color: Qt.rgba(0.02, 0.035, 0.06, 0.36)
                            border.width: 1
                            border.color: Qt.rgba(1, 1, 1, 0.08)

                            RowLayout {
                                anchors.fill: parent
                                anchors.margins: 8
                                spacing: 10

                                Text {
                                    text: modelData.label
                                    color: "#7f91aa"
                                    font.family: "Microsoft YaHei UI"
                                    font.pixelSize: 11
                                    Layout.preferredWidth: 92
                                }
                                Text {
                                    Layout.fillWidth: true
                                    text: modelData.value
                                    color: "#eaf2ff"
                                    font.family: "Consolas"
                                    font.pixelSize: 12
                                    elide: Text.ElideRight
                                }
                                GlassButton {
                                    text: page.s.copy
                                    fontSize: 11
                                    onClicked: backend.copy(modelData.value)
                                }
                            }
                        }
                    }

                    Text {
                        visible: backend.ipRows.length === 0
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        text: page.s.ipHint
                        color: "#65778f"
                        font.family: "Microsoft YaHei UI"
                        font.pixelSize: 12
                        wrapMode: Text.WordWrap
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    Item { Layout.fillHeight: true }
                }
            }

            GlassCard {
                backdrop: page.backdrop
                Layout.fillWidth: true
                Layout.fillHeight: true
                radius: 22

                ColumnLayout {
                    anchors.fill: parent
                    spacing: 6

                    Text {
                        text: page.s.subnetInfo
                        color: "#e8eef9"
                        font.family: "Microsoft YaHei UI"
                        font.pixelSize: 15
                        font.bold: true
                    }

                    Repeater {
                        model: backend.ipSubnetRows
                        delegate: Rectangle {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 40
                            radius: 9
                            color: Qt.rgba(0.02, 0.035, 0.06, 0.36)
                            border.width: 1
                            border.color: Qt.rgba(1, 1, 1, 0.08)

                            RowLayout {
                                anchors.fill: parent
                                anchors.margins: 8
                                spacing: 10

                                Text {
                                    text: modelData.label
                                    color: "#7f91aa"
                                    font.family: "Microsoft YaHei UI"
                                    font.pixelSize: 11
                                    Layout.preferredWidth: 92
                                }
                                Text {
                                    Layout.fillWidth: true
                                    text: modelData.value
                                    color: "#eaf2ff"
                                    font.family: "Consolas"
                                    font.pixelSize: 12
                                    elide: Text.ElideRight
                                }
                                GlassButton {
                                    text: page.s.copy
                                    fontSize: 11
                                    onClicked: backend.copy(modelData.value)
                                }
                            }
                        }
                    }

                    Text {
                        visible: !backend.ipHasSubnet
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        text: page.s.ipHint
                        color: "#65778f"
                        font.family: "Microsoft YaHei UI"
                        font.pixelSize: 12
                        wrapMode: Text.WordWrap
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    Item { Layout.fillHeight: true }
                }
            }
        }
    }

    Component.onCompleted: backend.parseIp("")

    Connections {
        target: backend
        function onLangChanged() { backend.parseIp(ipField.text) }
    }
}
