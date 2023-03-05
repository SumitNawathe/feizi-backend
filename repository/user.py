from typing import List, Optional

from sqlalchemy import MetaData, Table, Column, String, Integer, Boolean, Float, select, update, insert
from sqlalchemy import func
from sqlalchemy.engine import Engine
from sqlalchemy.engine.row import Row

from models.administration import User


class UserRepository:
    def __init__(self, sql_engine):
        self.sql_engine: Engine = sql_engine
        self.table_name = 'users'
        self.table_meta = MetaData(self.sql_engine)
        self.table = Table(
            self.table_name, self.table_meta,
            Column('id', Integer, primary_key=True),
            Column('username', String),
            Column('email', String),
            Column('password', String),
            schema='feizi'
        )

    def create(self, user: User) -> User:
        statement = insert(self.table).values(
            username=user.username,
            email=user.email,
            password=user.password
        )
        result = self.sql_engine.execute(statement)
        user._id = result.inserted_primary_key[0]
        return user

    def all(self) -> List[User]:
        statement = select(self.table).where(True)
        result = self.sql_engine.execute(statement)
        return list(map(lambda r: self._from_row(r), result))

    def get_by_username(self, username) -> Optional[User]:
        statement = select(self.table).where(self.table.c.username == username)
        result = self.sql_engine.execute(statement).first()
        if result is not None:
            return self._from_row(result)
        else:
            return None

    def _from_row(self, row: Row) -> User:
        return User(
            _id=row['id'],
            username=row['username'],
            email=row['email'],
            password=row['password']
        )
