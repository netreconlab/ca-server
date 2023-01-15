from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, create_engine, Relationship, Column, DateTime
from sqlalchemy.sql import func

from datetime import  datetime

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    username: str
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    creators: List["AppUser"] = Relationship(back_populates="creator")
    certificates: List["Certificate"] = Relationship(back_populates="user")

class AppUser(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # user_id:  int = Field(foreign_key="user.id")
    creator: User = Relationship(back_populates = "creators")
    certificates: Optional["Certificate"] = Relationship(back_populates="creator")

class Certificate(SQLModel, table=True):
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    creator: User = Relationship(back_populates="certificates")
    user: AppUser = Relationship(back_populates="certificate")


sqlite_file_name = "appdb.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()


    # created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    # created_at: datetime.datetime = Field(default=datetime.utcnow(), nullable=False)
    # updated_at: datetime = Field(
    #     sa_column= Column(
    #         DateTime(timezone=True),
    #         server_default=func.now(),
    #         nullable=False
    #     )
    # )
    # created_on = db.Column(db.DateTime, server_default=db.func.now())
    # updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    # date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    # date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    #                           onupdate=db.func.current_timestamp())