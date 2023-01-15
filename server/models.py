from uuid import uuid4

from peewee import *
from datetime import datetime
from .database import db

# class UnknownField(object):
#     def __init__(self, *_, **__): pass

class BaseModel(Model):
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db
#
# class SqliteSequence(BaseModel):
#     name = BareField(null=True)
#     seq = BareField(null=True)
#
#     class Meta:
#         table_name = 'sqlite_sequence'
#         primary_key = False

def genUUID():
    return str(uuid4())

# class User(BaseModel):
#     id = CharField(default=genUUID, primary_key=True)
#     username = CharField(unique=True)
#     password = CharField()

class AppUser(BaseModel):
    # id = CharField(default=genUUID, primary_key=True)
    id = CharField(primary_key=True)
    # creator = ForeignKeyField(field='id', model=User)

class Certificate(BaseModel):
    installation_id = CharField(column_name='installation_id', null=True)
    csr = CharField(null=True)
    certificate = CharField(null=True)
    # creator = ForeignKeyField(field='id', model=User)
    user = ForeignKeyField(field='id', model=AppUser, backref="certificates")

# db.connect()
#
MODELS = [
    # User,
    AppUser,
    Certificate,
]
#
# def create_tables ():
#     db.create_tables(MODELS)
#
# def drop_tables ():
#     db.drop_tables(MODELS)
#
#
# create_tables ()
# print(type(AppUser.select()))



