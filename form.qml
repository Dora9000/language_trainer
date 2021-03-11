import QtQuick 2.9
import QtQuick.Controls 2.15
import QtQuick.Window 2.0
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.15
Item {
    id:background
    width: 950; height: 600
    property var active_window: 3
    property var hat_size: 55
    property var menu_size: 150
    function append_sentence(sentence) {
        dataModel.insert(0,sentence)
    }
    function append_word(word) {
        dndModel.insert(0,word)
    }
    function append_word_to_sentence(word) {
        textModel.append(word)
    }
    function update_error_sentences(new_data) {
        let s_id = new_data[0]
        let e = new_data[1]

        for (let i = 0; i < dataModel.count; i++) {
            if (dataModel.get(i).sentence_id == s_id) {
            //text_editor.set_text(i);
                dataModel.setProperty(i, "err", e);
                break;
            }
        }
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
            anchors.topMargin: 15
            width: 150
            text: "Start solving"
            onClicked: {
            //text_editor.set_text(2);
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
                dataModel.clear()
                text_editor.update_sentences()


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
            //text_editor.set_text(1);
                active_window = 1
            }
        }
        Rectangle {
            opacity: 1
            color: "black"
            width: 2; height: parent.height
            anchors.left: active_window_button.right
        }
        MouseArea {
            id : menu_mouse
            anchors.fill: parent
            enabled : false
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
        visible: active_window == 2? true : false
        width: parent.width - menu_size; height: parent.height
        anchors.leftMargin: menu_size
        anchors.left: parent.left
        id: train_screen
        property bool train_started : false

        Rectangle {
            id: train_screen_0
            width: parent.width; height: parent.height
            anchors.top: parent.top
            anchors.right: parent.right
            color: "mistyrose"
            visible: !train_screen.train_started
            property int train_test : 0 //1
            property int level : 0
            Text {
                id: train_screen_text
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.leftMargin: 125
                anchors.topMargin: 60
                text: "Here you can start the language training. \n\nPlease select a difficulty level and training mode";
                font.pointSize: 12
                font.family: "Helvetica"
                font.weight: Font.Light
                horizontalAlignment: TextInput.AlignHCenter
            }

            Button {
                id: start_train_button
                property var taskExist : true
                visible: !train_screen.train_started
                height: 40
                width: 100
                text: "Start"
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.rightMargin: 25
                anchors.bottomMargin: parent.height / 2 + 15
                onClicked: {
                    text_editor.check_task_exist(train_screen_0.level,train_screen_0.train_test);
                    if (taskExist) {
                        train_screen_text.text = "Here you can start the language training. \n\nPlease select a difficulty level and training mode"
                        menu_mouse.enabled = true
                        text_editor.get_task(train_screen_0.level,train_screen_0.train_test)
                        train_screen.train_started = true
                        finish_sentence_button.visible = false
                        result.text = ""
                        //text_editor.set_text("hello from start_train_button");
                    } else {
                        text_editor.set_text("do not exist");
                        train_screen_text.text = "Test mode with this difficulty does not exist yet. \n\nTry different parameters"
                    }
                }
            }

            ButtonGroup {
                buttons: levels.children
                onClicked: {
                    if (button.text == "Light") {
                        train_screen_0.level = 0
                    }
                    if (button.text == "Middle") {
                        train_screen_0.level = 1
                    }
                    if (button.text == "Heavy") {
                        train_screen_0.level = 2
                    }
                }
            }

            Column {
                id: levels
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
                Label {
                    text: qsTr("Difficulty level")
                    font.pixelSize: 18
                    font.italic: true
                }
                RadioButton { text: "Light"; checked : true; font.pixelSize: 15 }
                RadioButton { text: "Middle"; font.pixelSize: 15 }
                RadioButton { text: "Heavy"; font.pixelSize: 15 }
            }

            ButtonGroup {
                buttons: types_train.children
                onClicked: {
                    if (button.text == "Train") {
                        train_screen_0.train_test = 0
                    } else {
                        train_screen_0.train_test = 1
                    }

                }
            }

            Column {
                id: types_train
                anchors.left: parent.left
                anchors.leftMargin: 125
                anchors.verticalCenter: parent.verticalCenter
                Label {
                    text: qsTr("Training mode")
                    font.pixelSize: 18
                    font.italic: true
                }
                RadioButton { text: "Train"; checked : true; font.pixelSize: 15}
                RadioButton { text: "Test"; font.pixelSize: 15 }
            }


        }


        Rectangle {
            width: parent.width; height: parent.height / 2
            anchors.top: parent.top
            anchors.right: parent.right
            color: "mistyrose"
            visible: train_screen.train_started


            Button {
                id: finish_sentence_button
                height: 40
                width: 100
                text: "Finish"
                visible : false
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.rightMargin: 135
                anchors.bottomMargin: 15
                onClicked: {
                    check_sentence_button.enabled = true
                    textModel.clear()
                    dndModel.clear()
                    train_screen.train_started = false
                    menu_mouse.enabled = false
                }
            }
            Button {
                id: check_sentence_button
                height: 40
                width: 100
                text: "Check"
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.rightMargin: 25
                anchors.bottomMargin: 15
                enabled : true
                onClicked: {
                    var finished = true
                    for (let i = 0; i < textModel.count; i++) {
                        if (textModel.get(i).active_drop) {
                            result.text = "Not finished"
                            finished = false
                        }
                    }
                    if (finished) {
                        text_editor.get_mark()
                        enabled = false
                        finish_sentence_button.visible = true
                        //text_editor.set_text("hello from check_sentence_button");
                    }
                }
            }
            Text {
                id : result
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.rightMargin: 50
                anchors.bottomMargin: 0
                text: ""
            }

            Rectangle {
                visible: true
                color: "white"
                width: parent.width - 50; height: parent.height - 100
                anchors.top: parent.top
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.topMargin: 30


                ListModel {
                    id: textModel
                    property var insertIndex : -1
                }

                Flow {
                    anchors.fill: parent
                    anchors.margins: 4
                    spacing: 2

                    Repeater {
                    id : repeaterGrid
                        model: textModel
                        Rectangle {
                            width: t_metrics.tightBoundingRect.width + 20
                            height: 40//t_metrics.tightBoundingRect.height + 10
                            property bool active_drop : model.active_drop
                            property bool caught_drop : false
                            color: active_drop?  "red" : "white";
                            radius: 5;

                            Text {
                                id: currentText
                                anchors.centerIn: parent
                                text: model.text;
                                font.pointSize: 15
                            }
                            TextMetrics {
                                id:     t_metrics
                                font:   currentText.font
                                text:   currentText.text
                            }

                            DropArea {
                                id: word_container0
                                anchors.fill: parent
                                onEntered: {
                                    if (parent.active_drop) {
                                        parent.opacity = 0.6
                                        //text_editor.set_text(dndGrid.draggedItemIndex)
                                        dndModel.set(dndGrid.draggedItemIndex, { color : "#80FF0000"})
                                        textModel.insertIndex = index
                                        //text_editor.set_text(index)
                                    }
                                }
                                onExited: {
                                parent.opacity = 1
                                    //text_editor.set_text("exit")
                                    dndModel.set(dndGrid.draggedItemIndex, { color : "white"})
                                    textModel.insertIndex = -1
                                }

                            }
                        }
                    }
                }
            }
        }



        // НИЖНЯЯ ПОЛОВИНА

        Rectangle {
            width: parent.width; height: parent.height / 2
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            color: "mistyrose"
            visible: train_screen.train_started

            Rectangle {
                visible: true
                color: "mistyrose"
                width: parent.width - 50; height: parent.height - 50
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter

                Component {
                    id: dndDelegate

                    Rectangle {
                        id: wrapper
                        width: 230
                        height: 35
                        color : model.color
                        Text {
                            text : model.text
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.horizontalCenter: parent.horizontalCenter
                        }

                        states: [

                                State {
                                    name: "greyedOut"
                                    when: (dndGrid.draggedItemIndex != -1) && !(dragArea.drag.active)
                                    PropertyChanges { target: wrapper; opacity: 0.5}
                                },
                                State {
                                    name: "inactive"
                                    when: !(dragArea.drag.active)
                                    PropertyChanges { target: wrapper; opacity: 1.0}
                                },


                            State {
                                name: "inDrag"
                                when: dragArea.drag.active
                                PropertyChanges { target: wrapper; width: 200 }
                                PropertyChanges { target: wrapper; height: 50 }
                                PropertyChanges { target: wrapper; parent: dndWordContainer }
                                PropertyChanges { target: wrapper; x: coords.mouseX}
                                PropertyChanges { target: wrapper; y: coords.mouseY}
                                PropertyChanges { target: dndGrid; draggedItemIndex : index }
                                PropertyChanges { target: imageBorder; opacity: 1 }
                            }
                        ]

                        Behavior on width { NumberAnimation { duration: 300; easing.type: Easing.OutQuint } }
                        Behavior on height { NumberAnimation { duration: 900; easing.type: Easing.OutElastic } }
                        Behavior on opacity { NumberAnimation { duration: 300; easing.type: Easing.InOutQuad } }

                        Drag.active: dragArea.drag.active
                        Drag.hotSpot.x: wrapper.width / 2
                        Drag.hotSpot.y: wrapper.height / 2
                        MouseArea {
                            id: dragArea
                            anchors.fill: parent
                            drag.target: parent
                            enabled : (dndModel.get(index).color == "white")

                            onReleased: {
                                if (textModel.insertIndex != -1) {
                                    var newPos = textModel.insertIndex
                                    var new_text = dndModel.get(index).text
                                    //text_editor.set_text(new_text);
                                    text_editor.write_answer(new_text, newPos);
                                    textModel.remove(newPos);
                                    textModel.insert(newPos,{text:new_text});
                                    dndModel.set(index, { color : "mistyrose", text : ""})
                                    dndGrid.draggedItemIndex = -1
                                    textModel.insertIndex = -1
                                }
                            }
                        }

                        Rectangle {
                            id: imageBorder
                            anchors.fill: parent
                            radius: 5
                            color: "transparent"
                            border.color: "red"
                            border.width: 6
                            opacity: 0
                        }
                    }
                }


                ListModel {
                    id: dndModel
                }

                GridView {
                    flow : GridView.FlowTopToBottom
                    id: dndGrid
                    anchors.fill: parent
                    interactive: false
                    cellWidth: 250
                    cellHeight: 50
                    model: dndModel
                    delegate: dndDelegate
                    property int draggedItemIndex: -1

                    Item {
                        id: dndWordContainer
                        anchors.fill: parent
                    }

                }
            }
        }
    }


    Item {
        /*
        Экран «Предложения»: позволяет редактировать список предложений, которые будут использоваться
        для генерации контрольных предложений – добавление, удаление, изменение. Напротив каждого
        элемента списка отображается количество допущенных ошибок
        */

        visible: (active_window == 0? true : false )
        width: parent.width - menu_size; height: parent.height
        anchors.leftMargin: menu_size
        anchors.left: parent.left



        Rectangle {
            id : font_blur0
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
                onClicked: {
                    dataModel.insert(0,{text: "", color: "bisque", err: "0", sentence_id : "-2"});
                    view.currentIndex = 0
                    text_input_back.opacity = 0.3;
                    text_input.visible = true;
                    text_input_button.visible = true;
                    //text_input_button_esc.visible = true;
                    text_input_back_area.enabled = true;
                    menu_mouse.enabled = true;
                }
            }


            Button {
                id: add_button2
                height: button_size
                anchors.left: add_button.right
                anchors.top: add_button.top
                anchors.leftMargin: 10
                width: 100
                text: "delete"
                onClicked: {
                    text_editor.rewrite_sentence("", dataModel.get(view.currentIndex).sentence_id)
                    dataModel.remove(view.currentIndex)
                }
            }


            Button {
                id: add_button3
                height: button_size
                width: 100
                text: "edit"
                anchors.left: add_button2.right
                anchors.top: add_button2.top
                anchors.leftMargin: 10
                onClicked: {
                    if (dataModel.count > 0) {
                        menu_mouse.enabled = true;
                        text_input_back.opacity = 0.4;
                        text_input.visible = true;
                        edit.text = dataModel.get(view.currentIndex).text;
                        text_input_button.visible = true;
                        text_input_button_esc.visible = true;
                        text_input_back_area.enabled = true;
                    }
                }
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
                    highlightMoveDuration : 200
                    //highlightMoveVelocity : 1000

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
                        property var sentence_id: model.sentence_id
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
                                text: model.err// + '/' + sentence_id
                                font.bold: isCurrent ? true : false
                            }

                        }
                    }
                }
            }

        }


        FastBlur {
            id: blurRectangleAndSubItems
            opacity: text_input.visible? 1 : 0
            visible: opacity !== 0

            anchors.fill: font_blur0
            source: font_blur0
            radius: 35
            Behavior on opacity {
                NumberAnimation {
                    duration: 500
                    easing.type: Easing.InOutQuad
                }
            }
        }
        Rectangle {
            id : text_input_back
            anchors.fill: parent
            color : "black"
            opacity : 0
            Behavior on opacity { NumberAnimation { duration: 300; easing.type: Easing.InOutQuad } }
            MouseArea {
                id : text_input_back_area
                anchors.fill: parent
                enabled : false
            }
        }
        Rectangle {
            id : text_input_title
            width: 500
            height: 40
            color : "tomato"
            radius: height / 2
            visible : text_input.visible
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: text_input.top
            anchors.bottomMargin: 20
            border {
                color: "black"
                width: 1
            }
            Text {
                anchors.centerIn: parent
                text: "Enter the text of the sentence"
                font.pixelSize: 15
            }
        }

        Rectangle {
            id : text_input
            width: 450
            height: 200
            color : "white"
            visible : false
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            Flickable {
                id: flick
                anchors.fill: parent
                contentWidth: edit.paintedWidth
                contentHeight: edit.paintedHeight
                clip: true


                function ensureVisible(r) {
                    if (contentX >= r.x) {
                        contentX = r.x;
                    }
                    else if (contentX+width <= r.x+r.width) {
                        contentX = r.x+r.width-width;
                    }
                    if (contentY >= r.y) {
                        contentY = r.y;
                    }
                    else if (contentY+height <= r.y+r.height) {
                        contentY = r.y+r.height-height;
                    }
                }

                TextInput {
                    id: edit
                    width: flick.width
                    focus: true
                    wrapMode: TextEdit.Wrap
                    onCursorRectangleChanged: flick.ensureVisible(cursorRectangle)
                    font.pixelSize: 17
                    selectByMouse: true
                    validator: RegExpValidator { regExp: /[^\s]+[A-Za-z\s]+$/ }
                }
            }
        }


        Button {
            id: text_input_button
            height: button_size
            width: 100
            visible : false
            enabled : (edit.text != "")
            text: "OK"
            anchors.left: text_input.right
            anchors.verticalCenter: parent.verticalCenter
            anchors.leftMargin: 20
            onClicked: {
                text_input_back.opacity = 0;
                text_input.visible = false;
                text_input_button.visible = false;
                var new_text = edit.text.replace(/ {1,}/g," "); //Удаление двойных пробелов
                new_text = new_text.trim(); //Удаление в начале и конце

                text_input_button_esc.visible = false;

                if (new_text != dataModel.get(view.currentIndex).text) {
                    dataModel.setProperty(view.currentIndex, "text", new_text);
                    dataModel.setProperty(view.currentIndex, "err", 0);
                    text_editor.rewrite_sentence(new_text, dataModel.get(view.currentIndex).sentence_id)
                }
                edit.text = "";
                text_input_back_area.enabled = false;
                menu_mouse.enabled = false;
            }
        }
        Button {
            id: text_input_button_esc
            height: button_size
            width: 100
            visible : false
            text: "Escape"
            anchors.left: text_input.right
            anchors.top: text_input_button.bottom
            anchors.topMargin: 20
            anchors.leftMargin: 20
            onClicked: {
                text_input_back.opacity = 0;
                text_input.visible = false;
                text_input_button.visible = false;
                text_input_button_esc.visible = false;
                edit.text = "";
                text_input_back_area.enabled = false;
                menu_mouse.enabled = false;

            }
        }
    }



    Connections {
        target: text_editor

        onSetResult: {}
        onGetTask : {}
        onWriteAnswer : {}
        onGetMark : {
            result.text = get_mark
        }
        onRewriteSentence : {
            dataModel.setProperty(view.currentIndex, "sentence_id", rewrite_sentence)
        }
        onUpdateSentences : {}
        onCheckTaskExist : {
            start_train_button.taskExist = check_task_exist
        }
    }
}