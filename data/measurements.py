import sqlalchemy
from .db_session import SqlAlchemyBase


class Measurements(SqlAlchemyBase):
    __tablename__ = 'measurements'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
