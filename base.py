from peewee import *
from settings import DB_FILE, DEBUG
import random

db = SqliteDatabase(DB_FILE)


class BaseModel(Model):
    class Meta:
        database = db


class Word(BaseModel):
    """
    Слово: Текст слова
    """
    id = PrimaryKeyField(null=False, unique=True)
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
    id = PrimaryKeyField(null=False, unique=True)  # error id
    sentence_id = ForeignKeyField(Sentence, to_field='sentence_id')
    word_id = ForeignKeyField(Word)  # word that need to be found

    class Meta:
        db_table = "Error"


class Error_words(BaseModel):
    """
    Номер ошибки - порядковые номера слов
    """
    error_id = ForeignKeyField(Error)  # error id
    word_id = ForeignKeyField(Word)  # word that need to be found

    class Meta:
        db_table = "Error_words"


class Task(BaseModel):
    """
    Задание: Предложение, Слова, Порядковые номера слов, Сложность задания
    сохранение целиком задания, которое было выполнено с ошибкой – с
    учётом того, какие слова были размещены заранее, а какие не были.
    """
    id = IntegerField(null=False)
    error_id = ForeignKeyField(Error)
    difficulty = IntegerField()

    class Meta:
        db_table = "Task"


def add_word(text):
    val = Word.select(fn.MAX(Word.id)).scalar()
    val = (0 if val is None else val) + 1
    try:
        row = Word.create(
            id=val,
            text=text,
        )
        row.save()
        return val
    except Exception as e:
        print(e)
        return None


def add_sentence(text):  # text is list
    assert (isinstance(text, list))
    val = Sentence.select(fn.MAX(Sentence.sentence_id)).scalar()
    val = (0 if val is None else val) + 1
    for i in range(len(text)):
        word = text[i]
        try:
            word = Word.select().where(Word.text == word).get()
        except DoesNotExist:
            print('Error. Word {0} does not exist'.format(word))
            return None
        except Exception as e:
            print(e)
            return None
        else:
            row = Sentence.create(
                sentence_id=val,
                word_id=word,
                order=i,
                length=len(text),
            )
            row.save()
    return val


def add_error(sentence_id, word_id):
    val = Error.select(fn.MAX(Error.id)).scalar()
    val = (0 if val is None else val) + 1
    try:
        row = Error.create(
            id=val,
            sentence_id=sentence_id,
            word_id=word_id,
        )
        row.save()
        return val
    except Exception as e:
        print(e)
        return None


def add_error_words(error_id, word_id):
    try:
        row = Error_words.create(
            error_id=error_id,
            word_id=word_id,
        )
        row.save()
    except Exception as e:
        print(e)


def add_task(error_ids, d):  # error_ids is list
    assert (isinstance(error_ids, list))
    val = Task.select(fn.MAX(Task.id)).scalar()
    i = (0 if val is None else val) + 1
    for error_id in error_ids:
        try:
            row = Task.create(
                id=i,
                difficulty=d,
                error_id=error_id,
            )
            row.save()
        except Exception as e:
            print(e)
            return None
    return i


def delete_error(id):
    err = Error.get(Error.id == id)
    err.delete_instance(recursive=True)  # delete error and all in Error_words


def delete_task(id):
    task = Task.get(Task.id == id)
    task.delete_instance()  # delete Task only


def get_word(id=None, cnt=1):
    if id is None:
        all_words = set(Word.select().text)
        assert(len(all_words) >= cnt)
        return random.sample(all_words, cnt)
    return Word.get(Word.id == id).text


def get_sentence(id=None, len=0):
    all_sentences = Sentence.select()
    if id is None:
        len_sentences = set()
        for sentence in all_sentences:
            if sentence.length >= len:
                len_sentences.append((sentence.sentence_id))
        id = random.sample(len_sentences, 1)

    words = []
    for sentence in all_sentences:
        if sentence.sentence_id == id:
            words.append([sentence.word_id,sentence.order])
    words.sort(key = lambda x: x[1])
    words = [words[i][0] for i in range(len(words))]
    words = [get_word(id=words[i]) for i in range(len(words))]
    return " ".join(words)



def init_db(database):
    database.create_tables([Word, Sentence, Error, Error_words, Task])
    add_word('I')
    add_word('love')
    add_word('books')
    add_sentence('I love books'.split(' '))
    add_word('like')
    add_sentence('I like books'.split(' '))
    id = add_error(1, 2)
    add_error_words(id, 4)
    add_word('We')

    add_task([1], 3)


try:
    db.connect()
    if DEBUG:
        init_db(db)

    for word in Word.select():
        print(word.text, word.id)

    for sentence in Sentence.select():
        print(sentence.sentence_id, sentence.word_id)

    # delete_error(1)
    print(Word.get(Word.id == 1).text)
    print('err')
    for e in Error.select():
        print(e.id, e.sentence_id)
    print('err_w')
    for e in Error_words.select():
        print(e.error_id, e.word_id)
    print('tasks')
    for e in Task.select():
        print(e.id, e.difficulty)

    db.close()
except InternalError as e:
    print(e)

print('hello from database')
