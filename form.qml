import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Window 2.0
import QtQuick.Layouts 1.15

Item {
    id:background
    width: 950; height: 600
    property var active_window: 3
    property var hat_size: 55
    property var menu_size: 150
    function append_sentence(sentence) {
        dataModel.insert(0,sentence)
    }

    Item {
        /*
        Меню
        слева -> начать тренировку, изменить предложения, выйти в меню
        */
        visible: true
        width: parent.width; height: parent.height
        anchors.left: parent.left
        Rectangle {
            opacity: 0.8
            color: "black"
            width: parent.width; height: parent.height
            Text {
                color: "white"
                id: he
                text: "Author: Baranova Daria"
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter

                font.pointSize: 10; font.bold: true
            }
        }

        property var button_size: 30
        Button {
            id: active_window_button
            visible: true
            height: button_size
            anchors.top: parent.top
            anchors.topMargin: 10
            width: 150
            text: "Start train"
            onClicked: {
                active_window = 2
            }
        }
        Button {
            id: active_window_button2
            visible: true
            height: button_size
            anchors.top: active_window_button.bottom
            anchors.topMargin: 10
            width: 150
            text: "Sentences"
            onClicked: {
                active_window = 0
            }
        }
        Button {
            id: active_window_button3
            visible: true
            height: button_size
            anchors.top: active_window_button2.bottom
            anchors.topMargin: 10
            width: 150
            text: "Other"
            onClicked: {
                active_window = 1
            }
        }


        Button {
            height: 40
            width: 40
            text: "set"
            anchors.horizontalCenter: parent.horizontalCenter
            onClicked: (text_editor.set_text("meow"))
        }

        Button {
            height: 40
            width: 40
            text: "NO"
            anchors.verticalCenter: parent.verticalCenter
            onClicked: calculator.sum("1","3")
        }

        Button {
            height: 60
            width: 60
            text: "get"
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            onClicked: text_editor.get_text()
        }

        Rectangle {
            height: 160
            width: 160
            x:150
            y:150
            color: "white"
            Text {
                id: sumResult
                text: "WTF"
            }

            Text {
                id: getResult
                anchors.verticalCenter: parent.verticalCenter
                text: "WTF2"
            }
        }
    }


    Item {
        /*
        Экран «Предложения»: позволяет редактировать список предложений, которые будут использоваться
        для генерации контрольных предложений – добавление, удаление, изменение. Напротив каждого
        элемента списка отображается количество допущенных ошибок
        */

        visible: (active_window == 1? false : true)
        width: parent.width - menu_size; height: parent.height
        anchors.leftMargin: menu_size
        anchors.left: parent.left

        Rectangle {
            color: "whitesmoke"
            width: parent.width; height: parent.height
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            property var button_size: 40
            Button {
                id: add_button
                height: button_size
                anchors.topMargin: 10
                width: 100
                text: "add"
                anchors.top: parent.top
                anchors.right: parent.right
                anchors.rightMargin: 230
                onClicked: (dataModel.insert(0,{text: "new", color: "bisque", err: "1"}))
            }


            Button {
                id: add_button2
                height: button_size
                anchors.left: add_button.right
                anchors.top: add_button.top
                anchors.leftMargin: 10
                width: 100
                text: "delete"
                onClicked: (dataModel.remove(view.currentIndex))
            }


            Button {
                id: add_button3
                height: button_size
                width: 100
                text: "edit"
                anchors.left: add_button2.right
                anchors.top: add_button2.top
                anchors.leftMargin: 10
                onClicked: (dataModel.setProperty(view.currentIndex, "text", "some new text"))
            }


            Rectangle {
                opacity: 1
                color: "whitesmoke"
                width: parent.width; height: (parent.height - hat_size)
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                anchors.topMargin: hat_size


                ListModel {
                    id: dataModel
                }

                ListView {
                    id: view
                    anchors.margins: 10
                    anchors.fill: parent
                    spacing: 10
                    model: dataModel
                    clip: true

                    highlight: Rectangle {
                        color: "skyblue"
                    }
                    highlightFollowsCurrentItem: true

                    header: Item {
                        id: listDelegate
                        property var view: ListView.view
                        property var isCurrent: ListView.isCurrentItem
                        width: view.width
                        height: hat_size
                        Rectangle {
                            anchors.margins: 5
                            anchors.fill: parent
                            anchors.rightMargin: (2 * height)
                            radius: height / 2
                            color: "tomato"
                            border {
                                color: "black"
                                width: 1
                            }
                            Text {
                                anchors.centerIn: parent
                                renderType: Text.NativeRendering
                                text: "Sentences with errors in solving"
                                font.bold: true
                            }
                        }
                    ScrollBar.vertical: ScrollBar {active: true}
                        Rectangle {
                            anchors.margins: 5
                            anchors.fill: parent
                            anchors.leftMargin: (parent.width - height - 35)
                            radius: height / 2
                            color: "tomato"
                            border {
                                color: "black"
                                width: 1
                            }
                            Text {
                                anchors.centerIn: parent
                                renderType: Text.NativeRendering
                                text: "Error"
                                font.bold: true
                            }

                        }
                    }

                    delegate: Item {
                        id: listDelegate
                        property var view: ListView.view
                        property var isCurrent: ListView.isCurrentItem
                        width: view.width
                        height: hat_size
                        Rectangle {
                            anchors.margins: 5
                            anchors.fill: parent
                            anchors.rightMargin: (2 * height)
                            radius: height / 2
                            color: model.color
                            border {
                                color: "black"
                                width: 1
                            }
                            Text {
                                anchors.centerIn: parent
                                renderType: Text.NativeRendering
                                text: "%1%2".arg(model.text).arg(isCurrent ? " *" : "")
                                font.bold: isCurrent ? true : false
                            }
                            MouseArea {
                                anchors.fill: parent
                                onClicked: view.currentIndex = model.index
                            }
                        }

                        Rectangle {
                            anchors.margins: 5
                            anchors.fill: parent
                            anchors.leftMargin: (parent.width - height - 35)
                            radius: height / 2
                            color: "tomato"
                            border {
                                color: "black"
                                width: 1
                            }
                            Text {
                                anchors.centerIn: parent
                                renderType: Text.NativeRendering
                                text: model.err
                                font.bold: isCurrent ? true : false
                            }
                        }
                    }
                }
            }
        }
    }




    Item {
        /*
        Экран «Тренировка»: содержит настройку «Сложность» и кнопку «Начать тренировку». После нажатия
        «Начать тренировку» отображаются задание и кнопка «Проверить». Задание – из базы выбирается
        предложение, на экране появляется предложение с пропусками и неразмещённые слова. «Сложность»
        определяет количество слов, которые нужно разместить. Кнопка «Проверить» проверяет расстановку,
        при наличии ошибок создаёт запись «Ошибка» в базе.
        */
        visible: true//active_window == 2? true : false
        width: parent.width - menu_size; height: parent.height
        anchors.leftMargin: menu_size
        anchors.left: parent.left



        Rectangle {
            opacity: 1
            color: "blue"
            width: parent.width; height: parent.height
        }

        Text {
            id: helloText
            text: "Hello world!"
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            font.pointSize: 10; font.bold: true
        }


        property int dif : 3

        Rectangle {
            width: parent.width
            height: parent.height / 2
            anchors.bottom: parent.bottom
            color: "#000000"

            Component {
                id: dndDelegate
                Item {
                    id: wrapper
                    width: dndGrid.cellWidth
                    height: dndGrid.cellHeight
                    Rectangle {
                        width: 50
                        height: 50
                        color: "red"
                    }
                }
            }

            ListModel {
                id: dndModel
                ListElement { }
                ListElement { }
                ListElement { }
                ListElement { }
                ListElement { }
                ListElement { }
                ListElement { }
                ListElement { }
                ListElement { }

            }

            GridView {
                id: dndGrid
                anchors.fill: parent
                anchors.margins: 10
                cellWidth: parent.wigth
                cellHeight: 100
                model: dndModel
                delegate: dndDelegate
            }
        }







    }


    Item {
        /*
        Экран «Тренировка на контрольных предложениях»: воспроизводит все задания (Tasks)
        */
    }


    Connections {
        target: text_editor
        onGetResult: {
            getResult.text = get_text
            //dataModel[0].text = "heee"
        }
        onSetResult: {}
    }

    Connections {
    target: calculator
        onSumResult: {
            // sum было задано через arguments=['sum']
            sumResult.text = sum
        }
    }
}