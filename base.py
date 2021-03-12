from peewee import *
from settings import DB_FILE, DEBUG, LOAD_DATA
import random
import os

if DEBUG:
    os.remove(DB_FILE)
db = SqliteDatabase(DB_FILE)


class BaseModel(Model):
    class Meta:
        database = db


class Word(BaseModel):
    """
    Слово: Текст слова
    """
    word_id = PrimaryKeyField(null=False, unique=True)
    text = CharField(max_length=100, unique=True)

    class Meta:
        db_table = "Word"


class Sentence(BaseModel):
    """
    Предложение: Слова, Порядковые номера слов
    """
    sentence_id = IntegerField(null=False)
    word_id = ForeignKeyField(Word)
    order = IntegerField(null=False)
    length = IntegerField(null=False)

    class Meta:
        db_table = "Sentence"


class Error(BaseModel):
    """
    Ошибка: Предложение, Слова, Порядковые номера слов, Сложность задания (?)
    """
    sentence_id = ForeignKeyField(Sentence, to_field='sentence_id')
    word_id = ForeignKeyField(Word)  # word that need to be found
    task_id = IntegerField(null=False)  # not unique, one task to many errors
    difficulty = IntegerField()
    word_to_check = BooleanField()

    class Meta:
        db_table = "Error"


def add_word(text):
    if len(text) == 0 or text == ' ':
        return -1
    val = Word.select(fn.MAX(Word.word_id)).scalar()
    val = (0 if val is None else val) + 1
    try:
        row = Word.create(
            word_id=val,
            text=text,
        )
        #row.save()
        return val

    except Exception as e:
        if e.args[0] == "UNIQUE constraint failed: Word.text":
            return None
        return None


def add_sentence(text):  # text is list
    assert (isinstance(text, list))
    val = Sentence.select(fn.MAX(Sentence.sentence_id)).scalar()
    val = (0 if val is None else val) + 1
    for i in range(len(text)):
        w = text[i]
        if len(w) == 0 or w == ' ':
            continue
        try:
            #w = Word.select().where(Word.text == w).get()
            w = Word.get(Word.text == w)
        except DoesNotExist:
            print('Error. Word {0} does not exist'.format(w.text))
            return None
        except Exception as e:
            print(e)
            return None
        else:
            row = Sentence.create(
                sentence_id=val,
                word_id=w.word_id,
                order=i,
                length=len(text),
            )
            #row.save()
    return val


def add_error(sentence_id, word_ids=None, word_texts=None):  # word_ids is list [(id,flag),(id,flag),...]
    if word_texts is not None:
        assert (isinstance(word_texts, list))
        word_ids = []
        for text, flag in word_texts:
            word = Word.get(Word.text == text)
            word_ids.append((word.word_id, flag))
        #print(word_ids)
    if word_ids is not None:
        assert (isinstance(word_ids, list))
        assert (Sentence.get(Sentence.sentence_id == sentence_id) is not None)
        val = Error.select(fn.MAX(Error.task_id)).scalar()
        val = (0 if val is None else val) + 1
        try:
            for word_id, flag in word_ids:
                row = Error.create(
                    task_id=val,
                    sentence_id=sentence_id,
                    word_id=word_id,
                    difficulty=(len(word_ids) % 5 + 1),
                    word_to_check=flag,
                )
                #row.save()
            return val
        except Exception as e:
            print(e)
            return None


def delete_error(task_id):
    err = Error.select().where(Error.task_id == task_id)
    for e in err:
        e.delete_instance(recursive=True)
    #print("errors deleted")


def delete_sentence(sentence_id):
    ss = Sentence.select().where(Sentence.sentence_id == sentence_id)
    for s in ss:
        s.delete_instance(recursive=True)
    err = Error.select().where(Error.sentence_id == sentence_id)
    for e in err:
        e.delete_instance(recursive=True)


def get_words(cnt=1):
    words_ = Word.select().order_by(fn.Random()).limit(cnt)
    words = []
    for word in words_:
        words.append(word.text)
    assert(len(words) == cnt)
    return words


def get_sentence(id=None, length=0, with_id=False):
    if id is None:
        len_sentences = set()
        for s in Sentence.select():
            if s.length >= length:
                len_sentences.add(s.sentence_id)
        id = random.sample(len_sentences, 1)[0]
    all_sentences = Sentence.select(Sentence.word_id, Sentence.order).where(Sentence.sentence_id == id)
    print(all_sentences)
    words = [[s.word_id.text, s.order] for s in all_sentences]

    words.sort(key=lambda x: x[1])
    words = [words[i][0] for i in range(len(words))]
    if with_id:
        return [" ".join(words), id]
    else:
        return " ".join(words)


def get_sentences(with_errors=False):
    # if with_errors == True -> calculate sum of tasks with errors in this sentence
    # [["the first sentence", errors],["the second sentence", errors],.....]
    # [["the first sentence"],["the second sentence"],.....]
    text = []
    if with_errors:
        for sentence in Sentence.select(Sentence.sentence_id).distinct():
            task_ids = Error.select(Error.task_id).where(Error.sentence_id == sentence.sentence_id).distinct()
            text.append([get_sentence(id=sentence.sentence_id), len(task_ids), sentence.sentence_id])
    else:
        for sentence in Sentence.select(Sentence.sentence_id).distinct():
            text.append([get_sentence(id=sentence.sentence_id)])
    return text


def check_task_exist_db(dif):
    try:
        query = Error.select().where(Error.difficulty == dif)
        if not query.exists():
            print('task with dif {0} do not exist'.format(dif))
            return False
    except Exception as e:
        print(e)
        return False
    return True


def get_task(dif):
    query = Error.select().where(Error.difficulty == dif)
    if not query.exists():
        print('task with dif {0} do not exist'.format(dif))
        raise Exception('base - get_task - task do not exist with dif = {0}'.format(dif))

    task_ = Error.select().where(Error.difficulty == dif).order_by(fn.Random()).limit(1)
    for task in task_:
        words_ = Error.select().where(Error.task_id == task.task_id)
        words = []
        for word in words_:
            words.append((word.word_id.text, word.word_to_check))
        random.shuffle(words)
        return [get_sentence(task.sentence_id.sentence_id), words, task.task_id]
    # ['I love books', ['hate', 'angry', 'love', 'We', 'like'], TASK_ID]


def init_db(database):
    database.create_tables([Word, Sentence, Error])
    s = ''
    if LOAD_DATA:
        with open("DATA.txt") as f:
            s = f.read()
        s = s.split('===')

        sentences = s[0].split('.')
        for sentence in sentences:
            st = sentence.strip()
            st = st.strip('\n')
            w = st.split(' ')
            if len(w) == 0:
                continue
            for word in w:
                add_word(word)
            add_sentence(st.split(' '))

        words = s[1].split(',')
        for word in words:
            word = word.strip('\n')
            word = word.strip()
            if len(word) == 0:
                continue
            add_word(word)

    for word in ["I", "love", "books", "like", "hate", "dinner", "smile", "angry", "sun", "education"]:
        add_word(word)

    add_sentence('A year has four seasons: spring, summer, autumn and winter'.split(' '))
    add_sentence('I love books'.split(' '))
    #add_sentence('I love smile'.split(' '))
    #add_word('We')
    if LOAD_DATA:
        id = add_error(sentence_id=1, word_ids=[(14, False), (2, True), (17, False), (12, False), (18, False)])
        id = add_error(sentence_id=3, word_ids=[(24, False), (9, True), (27, False), (22, False), (28, False)])
    #else:
        #id = add_error(sentence_id=1, word_ids=[(4, False), (2, True), (5, False), (6, False), (7, False)])
        #id = add_error(sentence_id=1, word_ids=[(4, False), (2, True), (5, False), (6, False), (8, False)])
        #id = add_error(sentence_id=1, word_ids=[(4, False), (2, True), (5, False), (6, False), (9, False)])

    #get_task(1)

try:
    db.connect()
    if DEBUG:
        init_db(db)

    db.close()
except InternalError as e:
    print(e)

print('hello from database')
for word in Word.select():
    print(word.text, word.word_id)
