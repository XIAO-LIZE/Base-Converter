import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"

Item {
    id: page

    property Item backdrop
    property var s: backend.strings
    property string query: ""
    property var ratios: [0.14, 0.14, 0.14, 0.21, 0.13, 0.24]

    function colWidth(i) {
        return page.tableWidth * ratios[i]
    }
    function headerText(i) {
        return [page.s.colDec, page.s.colHex, page.s.colOct,
                page.s.colBin, page.s.colChar, page.s.colDesc][i]
    }
    function applyRows(json) {
        var rows = JSON.parse(json)
        asciiModel.clear()
        for (var i = 0; i < rows.length; ++i)
            asciiModel.append(rows[i])
    }
    function reload() {
        backend.searchAscii(page.query)
    }

    ListModel { id: asciiModel }

    ColumnLayout {
        anchors.fill: parent
        spacing: 12

        GlassCard {
            backdrop: page.backdrop
            Layout.fillWidth: true
            Layout.preferredHeight: 196
            radius: 22

            ColumnLayout {
                anchors.fill: parent
                spacing: 12

                Text {
                    text: page.s.asciiLookup
                    color: theme.colors.text
                    font.family: "Microsoft YaHei UI"
                    font.pixelSize: 16
                    font.bold: true
                }

                GridLayout {
                    Layout.fillWidth: true
                    columns: 5
                    columnSpacing: 12
                    rowSpacing: 10

                    Text {
                        text: page.s.char
                        color: theme.colors.textSecondary
                        font.family: "Microsoft YaHei UI"
                        font.pixelSize: 13
                        Layout.preferredWidth: 82
                    }
                    GlassField {
                        id: charField
                        Layout.preferredWidth: 220
                        Layout.preferredHeight: 44
                        monospace: true
                        fontSize: 17
                        showClear: false
                        onEdited: backend.lookupChar(text)
                    }
                    GlassButton {
                        text: page.s.clear
                        Layout.alignment: Qt.AlignVCenter
                        onClicked: {
                            charField.text = ""
                            backend.lookupChar("")
                        }
                    }
                    Text {
                        Layout.fillWidth: true
                        Layout.columnSpan: 2
                        text: backend.charResult
                        color: backend.charTone === "warn" ? theme.colors.warning
                             : backend.charTone === "error" ? theme.colors.error : theme.colors.accent
                        font.family: "Consolas"
                        font.pixelSize: 13
                        elide: Text.ElideRight
                    }

                    Text {
                        text: page.s.decCode
                        color: theme.colors.textSecondary
                        font.family: "Microsoft YaHei UI"
                        font.pixelSize: 13
                        Layout.preferredWidth: 82
                    }
                    GlassField {
                        id: codeField
                        Layout.preferredWidth: 220
                        Layout.preferredHeight: 44
                        monospace: true
                        fontSize: 17
                        showClear: false
                        onEdited: backend.lookupCode(text)
                    }
                    GlassButton {
                        text: page.s.clear
                        Layout.alignment: Qt.AlignVCenter
                        onClicked: {
                            codeField.text = ""
                            backend.lookupCode("")
                        }
                    }
                    Text {
                        Layout.fillWidth: true
                        Layout.columnSpan: 2
                        text: backend.codeResult
                        color: backend.codeTone === "error" ? theme.colors.error : theme.colors.accent
                        font.family: "Consolas"
                        font.pixelSize: 13
                        elide: Text.ElideRight
                    }
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 12

            GlassField {
                id: searchField
                Layout.fillWidth: true
                Layout.preferredHeight: 46
                placeholder: page.s.searchPh
                showClear: false
                onEdited: {
                    page.query = text
                    backend.searchAscii(text)
                }
            }

            Text {
                text: backend.asciiCount
                color: theme.colors.textMuted
                font.family: "Microsoft YaHei UI"
                font.pixelSize: 12
            }

            GlassButton {
                text: page.s.all
                onClicked: {
                    searchField.text = ""
                    page.query = ""
                    backend.searchAscii("")
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
                    text: page.s.asciiTitle
                    color: theme.colors.text
                    font.family: "Microsoft YaHei UI"
                    font.pixelSize: 16
                    font.bold: true
                }

                Item {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 32

                    Row {
                        anchors.fill: parent
                        Repeater {
                            model: 6
                            delegate: Text {
                                width: page.colWidth(index)
                                height: parent.height
                                text: page.headerText(index)
                                color: theme.colors.accent
                                font.family: "Microsoft YaHei UI"
                                font.pixelSize: 12
                                font.bold: true
                                horizontalAlignment: index === 5 ? Text.AlignLeft
                                                                 : Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }
                        }
                    }
                }

                Item {
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    ListView {
                        id: tableList
                        anchors.fill: parent
                        clip: true
                        spacing: 2
                        model: asciiModel
                        ScrollBar.vertical: ScrollBar {
                            policy: ScrollBar.AsNeeded
                            contentItem: Rectangle {
                                implicitWidth: 6
                                radius: 3
                                color: theme.colors.scrollThumb
                            }
                            background: Rectangle { color: "transparent" }
                        }

                    delegate: Item {
                        width: ListView.view ? ListView.view.width : 0
                        height: 34

                        Rectangle {
                            anchors.fill: parent
                            radius: 7
                            color: index % 2 === 0 ? theme.colors.rowEven
                                                   : theme.colors.rowOdd
                        }

                        Row {
                            anchors.fill: parent

                            Text {
                                width: page.colWidth(0); height: parent.height
                                text: code; color: theme.colors.textCode
                                font.family: "Consolas"; font.pixelSize: 12
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }
                            Text {
                                width: page.colWidth(1); height: parent.height
                                text: hex; color: theme.colors.tableMuted
                                font.family: "Consolas"; font.pixelSize: 12
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }
                            Text {
                                width: page.colWidth(2); height: parent.height
                                text: oct; color: theme.colors.tableMuted
                                font.family: "Consolas"; font.pixelSize: 12
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }
                            Text {
                                width: page.colWidth(3); height: parent.height
                                text: bin; color: theme.colors.tableMuted
                                font.family: "Consolas"; font.pixelSize: 12
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }
                            Text {
                                width: page.colWidth(4); height: parent.height
                                text: char
                                color: parseInt(code) < 33 || parseInt(code) === 127
                                       ? theme.colors.warning : theme.colors.textValue
                                font.family: "Consolas"; font.pixelSize: 12
                                font.bold: true
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }
                            Text {
                                width: page.colWidth(5); height: parent.height
                                text: desc; color: theme.colors.textDesc
                                font.family: "Microsoft YaHei UI"; font.pixelSize: 12
                                horizontalAlignment: Text.AlignLeft
                                verticalAlignment: Text.AlignVCenter
                                elide: Text.ElideRight
                            }
                        }
                    }
                }

                    Text {
                        anchors.centerIn: parent
                        visible: asciiModel.count === 0
                        text: page.s.nors
                        color: theme.colors.textMuted
                        font.family: "Microsoft YaHei UI"
                        font.pixelSize: 13
                    }
                }
            }
        }
    }

    readonly property real tableWidth: tableList.width

    Component.onCompleted: backend.searchAscii("")

    Connections {
        target: backend
        function onAsciiResult(json) { page.applyRows(json) }
        function onLangChanged() { page.reload() }
    }
}
