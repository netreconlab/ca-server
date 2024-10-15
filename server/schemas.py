from typing import Any, List, Union
from datetime import datetime
import peewee
from pydantic import BaseModel

#class PeeweeModelGetter:
#    def get(self, key: Any, default: Any = None):
#        res = getattr(self._obj, key, default)
#        if isinstance(res, peewee.ModelSelect):
#            return list(res)
#        return res

class AppUserCreate(BaseModel):
    user: str

class AppUser(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime


    class Config:
        from_attributes = True
        #getter_dict = PeeweeModelGetter


class CertificateCreate(BaseModel):
    certificateId: str
    csr: str
    user: str

class CertificateUpdate(BaseModel):
    certificateId: str
    csr: str

class Certificate(BaseModel):
    certificate_id: str
    csr: str
    certificate: str
    user_id: str
    created_at: datetime
    updated_at: datetime


    class Config:
        from_attributes = True
        #getter_dict = PeeweeModelGetter
