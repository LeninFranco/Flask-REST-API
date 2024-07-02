from src.utils.db import db
from src.models.products import Product

class Category(db.Model):
    __tablename__ = 'Categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    products = db.relationship('Product', backref='category')

    def __init__(self, name) -> None:
        self.name = name