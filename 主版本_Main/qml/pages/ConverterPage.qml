import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"

Item {
    id: page

    property Item backdrop
    property var s: backend.strings
    property int baseIndex: 2

    property var resultRows: [
        { name: page.s.bases[0], value: backend.binary, color: "#10b981" },
        { name: page.s.bases[1], value: backend.octal, color: "#3b82f6" },
        { name: page.s.bases[2], value: backend.decimal, color: "#64748b" },
        { name: page.s.bases[3], value: backend.hexValue, color: "#f59e0b" }
    ]

    ColumnLayout {
        anchors.fill: parent
        spacing: 14

        GlassCard {
            backdrop: page.backdrop
            Layout.fillWidth: true
            Layout.preferredHeight: 200
            radius: 22

            ColumnLayout {
                anchors.fill: parent
                spacing: 10

                Text {
                    text: page.s.inputBase
                    color: "#8496ad"
                    font.family: "Microsoft YaHei UI"
                    font.pixelSize: 13
                    font.bold: true
                }

                Segmented {
                    id: bases
                    Layout.fillWidth: true
                    Layout.preferredHeight: 40
                    labels: page.s.bases
                    currentIndex: page.baseIndex
                    onActivated: function (index) {
                        page.baseIndex = index
                        backend.convert(field.text, index)
                    }
                }

                GlassField {
                    id: field
                    Layout.fillWidth: true
                    Layout.preferredHeight: 50
                    placeholder: page.s.inputHint
                    monospace: true
                    fontSize: 20
                    onEdited: backend.convert(field.text, page.baseIndex)
                }

                Text {
                    Layout.fillWidth: true
                    text: backend.convMessage
                    color: backend.convError ? "#ef4444" : "#7f91aa"
                    font.family: "Microsoft YaHei UI"
                    font.pixelSize: 12
                    elide: Text.ElideRight
                }
            }
        }

        GlassCard {
            backdrop: page.backdrop
            Layout.fillWidth: true
            Layout.fillHeight: true
            radius: 22

            ColumnLayout {
                anchors.fill: parent
                spacing: 8

                Text {
                    text: page.s.resultTitle
                    color: "#e8eef9"
                    font.family: "Microsoft YaHei UI"
                    font.pixelSize: 16
                    font.bold: true
                }

                Repeater {
                    model: page.resultRows
                    delegate: Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 64
                        radius: 14
                        color: Qt.rgba(0.02, 0.035, 0.06, 0.40)
                        border.width: 1
                        border.color: Qt.rgba(1, 1, 1, 0.09)

                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 10
                            spacing: 14

                            Rectangle {
                                Layout.preferredWidth: 102
                                Layout.fillHeight: true
                                radius: 9
                                color: Qt.rgba(0.35, 0.55, 0.9, 0.20)
                                border.width: 1
                                border.color: modelData.color
                                Text {
                                    anchors.centerIn: parent
                                    text: modelData.name
                                    color: modelData.color
                                    font.family: "Microsoft YaHei UI"
                                    font.pixelSize: 13
                                    font.bold: true
                                }
                            }

                            Text {
                                Layout.fillWidth: true
                                Layout.alignment: Qt.AlignVCenter
                                text: modelData.value === "" ? "—" : modelData.value
                                color: "#eaf2ff"
                                font.family: "Consolas"
                                font.pixelSize: 17
                                font.bold: true
                                wrapMode: Text.WrapAnywhere
                                maximumLineCount: 2
                                elide: Text.ElideRight
                            }

                            GlassButton {
                                text: page.s.copy
                                onClicked: backend.copy(modelData.value)
                            }
                        }
                    }
                }

                Item { Layout.fillHeight: true }
            }
        }
    }

    Component.onCompleted: backend.convert("", 2)

    Connections {
        target: backend
        function onLangChanged() {
            backend.convert(field.text, page.baseIndex)
        }
    }
}
