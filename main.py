import os
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView

from views import TextEditor, init_db, db
from settings import DB_FILE, DEBUG


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = QQuickView()
    view.setSource(QUrl('form.qml'))
    if DEBUG:
        os.remove(DB_FILE)
    try:
        db.connect()
        if DEBUG:
            init_db(db)
        print('start')

    except Exception as e:
        print(e)
    else:
        text_editor = TextEditor()
        view.engine().rootContext().setContextProperty("text_editor", text_editor)
        text_editor.init_data(db, view.rootObject())
        view.setTitle('Language trainer')
        view.show()
        app.exec_()
        db.close()
        sys.exit()
