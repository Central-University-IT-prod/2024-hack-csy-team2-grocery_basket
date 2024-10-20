import sqlalchemy
from .db_session import SqlAlchemyBase


class StorageConditions(SqlAlchemyBase):
    __tablename__ = 'storage_conditions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
