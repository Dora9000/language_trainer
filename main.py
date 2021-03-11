import sys

from views import *

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication#, QWidget
from PyQt5.QtQuick import QQuickView
#from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, QTimer, QDateTime, pyqtSlot
#from PyQt5.QtGui import QGuiApplication
#from PyQt5.QtQml import QQmlApplicationEngine
#from PyQt5 import QtWidgets
from PyQt5.QtCore import QMetaObject, Q_ARG, QVariant, QTimer, \
    QDate




if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = QQuickView()
    view.setSource(QUrl('form.qml'))
    #id = add_error(sentence_id=1, word_ids=[(14, False), (2, True), (17, False), (12, False), (18, False)])
    #id = add_error(sentence_id=3, word_ids=[(24, False), (9, True), (27, False), (22, False), (28, False)])
    calculator = Calculator()
    text_editor = TextEditor()

    view.engine().rootContext().setContextProperty("calculator", calculator)
    view.engine().rootContext().setContextProperty("text_editor", text_editor)
    text_editor.init_data(db, view.rootObject())
    view.setTitle('Language trainer')
    #init_form(view.rootObject())
    #add_words(view.rootObject(), ["my", "his"])
    #append_word_to_sentence(view.rootObject(), [("word1", False),("..........", True),("word3", False),("..........", True),("word5", False)])
    #update_error_sentences(view.rootObject(), 2, 7)
    print('start work')
    view.show()
    sys.exit(app.exec_())

    s = '''
    
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    calculator = Calculator()
    text_editor = TextEditor()
    ctx.setContextProperty("calculator", calculator)  # the string can be anything
    ctx.setContextProperty("text_editor", text_editor)
    engine.load('form.qml')
    window = engine.rootObjects()[0]
    window.show()
    sys.exit(app.exec_())
    '''

    s = '''
    
    
    
"""
counter = 0
def onTimeout(obj):
    global counter
    value = {"text": "Dora top", "color": "bisque", "err": str(counter)}
    #value = {"lesson": str(counter), "subject": "PE", "day": QDate.longDayName(1 + counter % 7)}
    QMetaObject.invokeMethod(obj, "append_sentence", Q_ARG(QVariant, value))
    counter += 1
    
    
    
    
    
    in main 
    #timer = QTimer()
    #timer.timeout.connect(lambda: onTimeout(view.rootObject()))
    #timer.start(1000)
"""
    
    
    
    
    
    
    class Main(QObject):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.view = QQuickView()
        self.view.setSource(QUrl('form.qml'))
        self.view.setTitle('Language trainer')

    def connect(self, myClass, name):
        self.view.engine().rootContext().setContextProperty(name, myClass)

    def show(self):
        self.view.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.connect(Calculator(), "calculator")
    main.connect(TextEditor(), "text_editor")
    main.show()
    sys.exit(app.exec_())
    '''

s = '''

class DragDropListView(QtWidgets.QListView):
    # This is the library listview
    def __init__(self, main_window, parent):
        super(DragDropListView, self).__init__(parent)
        self.main_window = main_window
        self.setAcceptDrops(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setResizeMode(QtWidgets.QListView.Fixed)
        self.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.setViewMode(QtWidgets.QListView.IconMode)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setProperty("showDropIndicator", False)
        self.setProperty("isWrapping", True)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setUniformItemSizes(True)
        self.setWordWrap(True)
        self.setObjectName("listView")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(DragDropListView, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(DragDropListView, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            file_list = [url.path() for url in event.mimeData().urls()]
            self.main_window.process_post_hoc_files(file_list, False)
            event.acceptProposedAction()
        else:
            super(DragDropListView, self).dropEvent(event)
'''
