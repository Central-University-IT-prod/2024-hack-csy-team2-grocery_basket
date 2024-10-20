import sqlalchemy
from .db_session import SqlAlchemyBase


class Food(SqlAlchemyBase):
    __tablename__ = 'foods'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    purchase_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    storage_life = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=1)
    count_units = sqlalchemy.Column(sqlalchemy.String, nullable=False, default="шт")
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
