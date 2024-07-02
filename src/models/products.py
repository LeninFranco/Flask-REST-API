from src.utils.db import db

class Product(db.Model):
    __tablename__ = 'Products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    idCategory = db.Column(db.Integer, db.ForeignKey('Categories.id'), nullable=False)

    def __init__(self, name, description, price, idCategory) -> None:
        self.name = name
        self.description = description
        self.price = price
        self.idCategory = idCategory