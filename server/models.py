from uuid import uuid4

from peewee import *
from datetime import datetime
from .database import db

class BaseModel(Model):
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db

def genUUID():
    return str(uuid4())

class AppUser(BaseModel):
    id = CharField(primary_key=True)

class Certificate(BaseModel):
    certificate_id = CharField(column_name='certificate_id', null=True)
    csr = CharField(null=True)
    certificate = CharField(null=True)
    user = ForeignKeyField(field='id', model=AppUser, backref="certificates")

MODELS = [
    AppUser,
    Certificate,
]
