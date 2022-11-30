from peewee import *

db = SqliteDatabase('notofocations.db')


class TextNotification(Model):
    chat_id = IntegerField()
    payload = CharField()
    time = DateTimeField()

    class Meta:
        database = db  # модель будет использовать базу данных 'people.db'
