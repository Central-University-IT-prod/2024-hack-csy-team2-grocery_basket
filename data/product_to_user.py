import sqlalchemy
from .db_session import SqlAlchemyBase


class ProductToUser(SqlAlchemyBase):
    __tablename__ = 'user-products'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id"), nullable=False)
    creation_date = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    measurement_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("measurements.id"), nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    storage_conditions_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("storage_conditions.id"), nullable=False)
