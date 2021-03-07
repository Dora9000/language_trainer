from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, QTimer, QDateTime, pyqtSlot


class Calculator(QObject):
    def __init__(self):
        QObject.__init__(self)

    # cигнал передающий сумму
    # обязательно даём название аргументу через arguments=['sum']
    # иначе нельзя будет его забрать в QML
    sumResult = pyqtSignal(int, arguments=['sum'])
    subResult = pyqtSignal(int, arguments=['sub'])

    # слот для суммирования двух чисел
    @pyqtSlot(int, int)
    def sum(self, arg1, arg2):
        # складываем два аргумента и испускаем сигнал
        self.sumResult.emit(arg1 + arg2)

    # слот для вычитания двух чисел
    @pyqtSlot(int, int)
    def sub(self, arg1, arg2):
        # вычитаем аргументы и испускаем сигнал
        self.subResult.emit(arg1 - arg2)


class TextEditor(QObject):
    def __init__(self):
        QObject.__init__(self)

    getResult = pyqtSignal(str, arguments=['get_text'])
    setResult = pyqtSignal(arguments=['set_text'])

    @pyqtSlot()
    def get_text(self):
        print("get slot")
        self.getResult.emit('hello')

    @pyqtSlot(str)
    def set_text(self, text):
        print(text)
        self.setResult.emit()



