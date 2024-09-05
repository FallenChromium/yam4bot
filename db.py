from enum import unique
from peewee import Model, IntegerField, CharField, SqliteDatabase

db = SqliteDatabase('bot.db')
db.connect()


class CachedAudio(Model):
    id = IntegerField(index=True, unique=True, primary_key=True)
    yam_id = CharField(unique=True)
    tg_file_id = CharField(unique=True)

    class Meta:
        database = db


db.create_tables([CachedAudio])


def get(yam_id: str) -> CachedAudio | None:
    return CachedAudio.get_or_none(CachedAudio.yam_id == yam_id)

def save(yam_id:str, tg_file_id: str):
    return CachedAudio(yam_id=yam_id, tg_file_id=tg_file_id).save()
