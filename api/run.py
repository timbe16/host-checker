from peewee import CharField, IntegerField, DoubleField, PostgresqlDatabase, Model
import datetime
import os
from sanic import Sanic
from sanic_crud import generate_crud

pg_db = PostgresqlDatabase(os.getenv('POSTGRES_DB'), user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASSWORD'), host='db')


class BaseModel(Model):
    class Meta:
        database = pg_db


class Urlcheck(BaseModel):
    url = CharField()
    check_datetime = CharField()
    duration = DoubleField()
    response_code = IntegerField()


app = Sanic(__name__)
generate_crud(app, [Urlcheck])
app.run(host="0.0.0.0", port=8000, debug=True)
