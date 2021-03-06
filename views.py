from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from base import *
import random
from PyQt5.QtCore import QMetaObject, Q_ARG, QVariant


def add_words(obj, words_list, empty=False):
    color = "white" if not empty else "mistyrose"
    for word in words_list:
        value = {"color": color, "text": word}
        QMetaObject.invokeMethod(obj, "append_word", Q_ARG(QVariant, value))


def append_word_to_sentence(obj, words_list):
    for word, flag in words_list:
        value = {"text": word, "active_drop": flag}
        QMetaObject.invokeMethod(obj, "append_word_to_sentence", Q_ARG(QVariant, value))


def init_form(obj, sentences):
    for i in range(len(sentences)):
        value = {"text": sentences[i][0], "color": "bisque", "err": str(sentences[i][1]),
                 "sentence_id": str(sentences[i][2])}
        QMetaObject.invokeMethod(obj, "append_sentence", Q_ARG(QVariant, value))


def update_error_sentences(obj, s_id, e):
    QMetaObject.invokeMethod(obj, "update_error_sentences", Q_ARG(QVariant, [s_id, e]))


def make_new_task(dif):
    """
    Make new task to solve from random sentence
    :param dif: 1-3
    :return: [[("word1", False),("word2", True)], [words with correct], sentence_id]
    """
    sentence = get_sentence(length=dif * 2, with_id=True)
    sentence_id = sentence[1]
    sentence = sentence[0].split(' ')
    words = [i for i in range(len(sentence))]
    words_to_check = set(random.sample(words, dif))  # numbers
    answer_1 = [(sentence[i], i in words_to_check) for i in range(len(sentence))]
    words_to_check = set([sentence[i] for i in words_to_check])
    words = get_words(cnt=dif * 5)
    uniq_words = []
    for word in words:
        if word not in words_to_check:
            uniq_words.append((word, False))
    words_to_check = list(words_to_check)
    return [answer_1, uniq_words[:dif * 4] + [(words_to_check[i], True) for i in range(len(words_to_check))],
              sentence_id]


def make_old_task(dif):
    """
    Make task from existed in DB
    :param dif: 1-3
    :return: [[("word1", False),("word2", True)], [words with correct], task_id]
    """
    data = get_task(dif)
    sentence_ = data[0].split(' ')
    words_ = data[1]
    words_to_check = set()
    for word, flag in words_:
        if flag:
            words_to_check.add(word)
    sentence = [(sentence_[i], sentence_[i] in words_to_check) for i in range(len(sentence_))]
    return [sentence, words_, data[2]]


class TextEditor(QObject):
    def __init__(self):
        QObject.__init__(self)

    setResult = pyqtSignal(arguments=['set_text'])
    getTask = pyqtSignal(arguments=['get_task'])
    writeAnswer = pyqtSignal(arguments=['write_answer'])
    getMark = pyqtSignal(list, arguments=['get_mark'])
    rewriteSentence = pyqtSignal(int, arguments=['rewrite_sentence'])
    updateSentences = pyqtSignal(arguments=['update_sentences'])
    checkTaskExist = pyqtSignal(bool, arguments=['check_task_exist'])

    db = None
    obj = None

    MISTAKES = 0
    correct_words = []  # [("word1", False),("word2", True),.....] #full sentence
    all_words = []
    TASK_ID = -1
    SENTENCE_ID = -1


    def init_data(self, database, obj_):
        self.db = database
        self.obj = obj_

    @pyqtSlot(str)
    def set_text(self, text):
        print(text)
        self.setResult.emit()

    @pyqtSlot(int, int)
    def get_task(self, difficulty, task_type):  # TRAIN 0, TEST 1
        difficulty += 1
        words = None
        data = None
        if task_type == 1:
            data = make_old_task(difficulty)
            self.TASK_ID = data[2]
            self.correct_words = data[0]
            random.shuffle(data[1])
            words = data[1]
        else:
            data = make_new_task(difficulty)
            self.SENTENCE_ID = data[2]
            self.correct_words = data[0]
            random.shuffle(data[1])
            words = data[1]
        self.all_words = words
        s = []
        for word, flag in self.correct_words:
            if flag:
                s.append((".........", flag))
            else:
                s.append((word, flag))
        append_word_to_sentence(self.obj, s)
        add_words(self.obj, [words[i][0] for i in range(len(words))])
        if difficulty == 1:
            add_words(self.obj, ["", "", "", "", ""], True)
        self.getTask.emit()

    @pyqtSlot(str, int)
    def write_answer(self, word, index):
        #print(self.correct_words[index][0], word)
        if self.correct_words[index][0] != word:
            self.MISTAKES += 1
        self.writeAnswer.emit()

    @pyqtSlot()
    def get_mark(self):
        if self.TASK_ID == -1:  # train mode
            if self.MISTAKES > 0:
                id = add_error(sentence_id=self.SENTENCE_ID, word_texts=self.all_words)  # all_words
            else:
                print('train mode. nothing to do')
        else:  # test mode
            if self.MISTAKES > 0:
                print('test mode. nothing to do')
            else:
                delete_error(self.TASK_ID)

        answer = ""
        if self.MISTAKES > 0:
            answer = str(self.MISTAKES) + " mistake"
            if self.MISTAKES > 1:
                answer += "s"
        else:
            answer = "Correct!"

        s = ""
        for word_, flag_ in self.correct_words:
            s += word_ + ' '
        s = s[:-1]
        self.correct_words = []
        self.TASK_ID = -1
        self.SENTENCE_ID = -1
        self.MISTAKES = 0
        self.getMark.emit([answer, s])

    @pyqtSlot(str, int)
    def rewrite_sentence(self, sentence, id):
        if sentence == "":  # delete sentence
            delete_sentence(id)
            new_id = -1  # does not matter

        elif id == -2:  # add sentence to DB
            words = sentence.split(' ')
            for word in words:
                add_word(word)
            new_id = add_sentence(sentence.split(' '))

        else:  # rewrite sentence and make err = 0 (delete tasks)
            delete_sentence(id)
            words = sentence.split(' ')
            for word in words:
                add_word(word)
            new_id = add_sentence(sentence.split(' '))

        self.rewriteSentence.emit(new_id)  # new id if add or old if deleted/rewrited (will refresh sentence_id anyway)

    @pyqtSlot()
    def update_sentences(self):  # fill Sentences screen
        data = get_sentences(True)
        init_form(self.obj, data)
        self.updateSentences.emit()

    @pyqtSlot(int, int)
    def check_task_exist(self, difficulty, task_type):  # TRAIN 0, TEST 1
        difficulty += 1
        exists = True
        if task_type == 1:
            exists = check_task_exist_db(difficulty)
        else:
            try:
                sentence = get_sentence(length=difficulty * 2, with_id=True)
                words = get_words(cnt=difficulty * 5)
            except Exception as e:
                print('cant create task')
                print(e)
                exists = False
        print("task exists : ", exists)
        self.checkTaskExist.emit(exists)
