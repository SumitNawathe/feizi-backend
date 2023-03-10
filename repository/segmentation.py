from typing import List, Optional

from sqlalchemy import MetaData, Table, Column, String, Integer, Boolean, Float, select, update, insert, ForeignKey
from sqlalchemy import func
from sqlalchemy.engine import Engine
from sqlalchemy.engine.row import Row

from app import LOG
from models.administration import User, UploadedImage, Segmentation
import json


class SegmentationRepository:
    def __init__(self, sql_engine):
        self.sql_engine: Engine = sql_engine
        self.table_name = 'segmentations'
        self.table_meta = MetaData(self.sql_engine)
        self.table = Table(
            self.table_name, self.table_meta,
            Column('id', Integer, primary_key=True),
            Column('image_id', String, ForeignKey('uploaded_images.id')),
            Column('points', String),
            schema='feizi'
        )

    def create(self, segmentation: Segmentation) -> Segmentation:
        points = json.dumps(segmentation.points)
        statement = insert(self.table).values(
            image_id=segmentation.image_id,
            points=points
        )
        result = self.sql_engine.execute(statement)
        segmentation._id = result.inserted_primary_key[0]
        return segmentation
