import peewee


db = peewee.SqliteDatabase('albums.db')


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Album(BaseModel):
    id = peewee.IntegerField(unique=True)
    titulo = peewee.CharField()

class Photos(BaseModel):
    id = peewee.IntegerField(unique=True)
    titulo = peewee.CharField()
    url = peewee.CharField()
    thumb = peewee.CharField()
    album_id = peewee.IntegerField()