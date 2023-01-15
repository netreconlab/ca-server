from typing import Any, List, Union
from datetime import datetime
import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict

class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res

# class UserCreate(BaseModel):
#     username: str
#     password: str
#
# class User(BaseModel):
#     id :str
#     username: str
#     created_at: datetime
#     updated_at: datetime
#
#
#     class Config:
#         orm_mode = True
#         getter_dict = PeeweeGetterDict
#


class AppUserCreate(BaseModel):
    user: str
    # authenticatedUserId: str

class AppUser(BaseModel):
    id: str
    # user: str
    # creator: User
    created_at: datetime
    updated_at: datetime


    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class CertificateCreate(BaseModel):
    installationId: str
    csr: str
    user: str

class CertificateUpdate(BaseModel):
    installationId: str
    csr: str

class Certificate(BaseModel):
    installation_id: str
    csr: str
    certificate: str
    # creator: User
    user_id: str
    created_at: datetime
    updated_at: datetime


    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict