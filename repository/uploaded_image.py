from typing import List, Optional

from sqlalchemy import MetaData, Table, Column, String, Integer, Boolean, Float, select, update, insert, ForeignKey
from sqlalchemy import func
from sqlalchemy.engine import Engine
from sqlalchemy.engine.row import Row

from models.administration import User, UploadedImage


class UploadedImageRepository:
    def __init__(self, sql_engine):
        self.sql_engine: Engine = sql_engine
        self.table_name = 'uploaded_images'
        self.table_meta = MetaData(self.sql_engine)
        self.table = Table(
            self.table_name, self.table_meta,
            Column('id', Integer, primary_key=True),
            Column('user_id', String, ForeignKey('user.id')),
            Column('filename', String),
            schema='feizi'
        )

    def create(self, image: UploadedImage) -> UploadedImage:
        statement = insert(self.table).values(
            user_id=image.user_id,
            filename=image.filename,
        )
        result = self.sql_engine.execute(statement)
        image._id = result.inserted_primary_key[0]
        return image

    def all(self) -> List[UploadedImage]:
        statement = select(self.table).where(True)
        result = self.sql_engine.execute(statement)
        return list(map(lambda r: self._from_row(r), result))

    def get_for_user_id(self, user_id) -> List[UploadedImage]:
        statement = select(self.table).where(self.table.c.user_id == user_id)
        result = self.sql_engine.execute(statement)
        return list(map(lambda r: self._from_row(r), result))

    def _from_row(self, row: Row) -> UploadedImage:
        return UploadedImage(
            _id=row['id'],
            user_id=row['user_id'],
            filename=row['filename']
        )
