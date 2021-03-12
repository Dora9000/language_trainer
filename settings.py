
DB_FILE = 'base.db'
DEBUG = False
LOAD_DATA = False
"""
            Rectangle {
                id: answer_sentence
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: check_sentence_button.left
                anchors.leftMargin: 25
                anchors.rightMargin: 25
                anchors.bottomMargin: 15

                property var answer_text_ : ""
                height: 40
                //width: 100
                color: "mistyrose"
                Text {
                    text: parent.answer_text_ 
                    anchors.fill: parent
                    anchors.centerIn: parent
                    font.pointSize: 12
                }
            }
"""