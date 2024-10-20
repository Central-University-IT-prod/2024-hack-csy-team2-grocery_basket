import sqlalchemy
from sqlalchemy import nullsfirst, ForeignKey

from .db_session import SqlAlchemyBase


class Products(SqlAlchemyBase):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    freshness_duration = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    category_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey("products.category_id"), nullable=False)


