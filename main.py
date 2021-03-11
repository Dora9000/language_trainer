import sys

from views import TextEditor, db
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = QQuickView()
    view.setSource(QUrl('form.qml'))
    #id = add_error(sentence_id=1, word_ids=[(14, False), (2, True), (17, False), (12, False), (18, False)])
    #id = add_error(sentence_id=3, word_ids=[(24, False), (9, True), (27, False), (22, False), (28, False)])
    text_editor = TextEditor()

    view.engine().rootContext().setContextProperty("text_editor", text_editor)
    text_editor.init_data(db, view.rootObject())
    view.setTitle('Language trainer')

    view.show()
    sys.exit(app.exec_())
