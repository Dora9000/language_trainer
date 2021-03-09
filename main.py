import sys
from base import *
from views import *

from PyQt5.QtCore import QUrl  # Класс QUrl предоставляет удобный интерфейс для работы с Urls
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtQuick import QQuickView  # Класс QQuickView предоставляет возможность отображать QML файлы.
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, QTimer, QDateTime, pyqtSlot
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5 import QtWidgets
from PyQt5.QtCore import QMetaObject, Q_ARG, QVariant, QTimer, \
    QDate


def add_words(obj, words_list):
    for word in words_list:
        value = {"color" : "white", "text" : word}
        QMetaObject.invokeMethod(obj, "append_word", Q_ARG(QVariant, value))


def append_word_to_sentence(obj, words_list):  # random sort
    for word, flag in words_list:
        value = {"text": word, "active_drop": flag}
        QMetaObject.invokeMethod(obj, "append_word_to_sentence", Q_ARG(QVariant, value))


def init_form(obj):
    # add sentences with/without errors
    for i in range(4):
        value = {"text": "Dora top", "color": "bisque", "err": "5"}
        QMetaObject.invokeMethod(obj, "append_sentence", Q_ARG(QVariant, value))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = QQuickView()
    view.setSource(QUrl('form.qml'))

    calculator = Calculator()
    text_editor = TextEditor()
    view.engine().rootContext().setContextProperty("calculator", calculator)
    view.engine().rootContext().setContextProperty("text_editor", text_editor)
    view.setTitle('Language trainer')
    #init_form(view.rootObject())
    add_words(view.rootObject(), ["my", "his"])
    append_word_to_sentence(view.rootObject(), [("word1", False),("..........", True),("word3", False),("..........", True),("word5", False)])
    view.show()
    sys.exit(app.exec_())
