from peewee import *
from settings import DB_FILE, DEBUG
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

    class Meta:
        db_table = "Error"


def add_word(text):
    val = Word.select(fn.MAX(Word.word_id)).scalar()
    val = (0 if val is None else val) + 1
    try:
        row = Word.create(
            word_id=val,
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
        w = text[i]
        try:
            w = Word.select().where(Word.text == w).get()
        except DoesNotExist:
            print('Error. Word {0} does not exist'.format(w))
            return None
        except Exception as e:
            print(e)
            return None
        else:
            row = Sentence.create(
                sentence_id=val,
                word_id=w,
                order=i,
                length=len(text),
            )
            row.save()
    return val


def add_error(sentence_id, word_ids):  # word_ids is list
    assert (isinstance(word_ids, list))
    assert (Sentence.get(Sentence.sentence_id == sentence_id) is not None)
    val = Error.select(fn.MAX(Error.task_id)).scalar()
    val = (0 if val is None else val) + 1
    try:
        for word_id in word_ids:
            row = Error.create(
                task_id=val,
                sentence_id=sentence_id,
                word_id=word_id,
                difficulty=len(word_ids),
            )
            row.save()
        return val
    except Exception as e:
        print(e)
        return None


def delete_error(task_id):
    err = Error.get(Error.task_id == task_id)
    err.delete_instance(recursive=True)


def get_word(id=None, cnt=1):
    if id is None:
        all_words = set(Word.select().text)
        assert(len(all_words) >= cnt)
        return random.sample(all_words, cnt)
    return Word.get(Word.word_id == id).text


def get_sentence(id=None, length=0):
    all_sentences = Sentence.select()
    if id is None:
        len_sentences = set()
        for s in all_sentences:
            if s.length >= length:
                len_sentences.add(s.sentence_id)
        id = random.sample(len_sentences, 1)

    words = []
    for s in all_sentences:
        if s.sentence_id == id:
            words.append([s.word_id, s.order])
    words.sort(key=lambda x: x[1])
    words = [words[i][0] for i in range(len(words))]
    words = [get_word(id=words[i]) for i in range(len(words))]
    return " ".join(words)


def get_sentences(with_errors=False):
    # if with_errors == True -> calculate sum of tasks with errors in this sentence
    # [["the first sentence", errors],["the second sentence", errors],.....]
    # [["the first sentence"],["the second sentence"],.....]
    text = []
    if with_errors:
        for sentence in Sentence.select(Sentence.sentence_id).distinct():
            task_ids = Error.select(Error.task_id).where(Error.sentence_id == sentence.sentence_id).distinct()
            text.append([get_sentence(id=sentence.sentence_id), len(task_ids)])
    else:
        for sentence in Sentence.select(Sentence.sentence_id).distinct():
            text.append([get_sentence(id=sentence.sentence_id)])
    return text


def init_db(database):
    database.create_tables([Word, Sentence, Error])
    add_word('I')
    add_word('love')
    add_word('books')
    add_sentence('I love books'.split(' '))
    add_word('like')
    add_word('hate')
    add_word('smile')
    add_word('angry')
    add_sentence('I books'.split(' '))
    add_sentence('I smile'.split(' '))

    id = add_error(sentence_id=2, word_ids=[4, 3, 1])
    id = add_error(sentence_id=2, word_ids=[2, 3, 1])

    add_word('We')


try:
    db.connect()
    if DEBUG:
        init_db(db)


    db.close()
except InternalError as e:
    print(e)

print('hello from database')


