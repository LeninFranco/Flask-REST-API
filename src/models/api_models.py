from flask_restx import fields
from src.utils.api import api

#Product

product_model = api.model('Product', {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'price': fields.Float
})

category_model = api.model('Category', {
    'id': fields.Integer,
    'name': fields.String,
    'products': fields.List(fields.Nested(product_model))
})

category_input_model = api.model('CategoryInput', {
    'name': fields.String
})

product_model_with_category = api.model('ProductCategory', {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'price': fields.Float,
    'category': fields.Nested(category_input_model)
})

product_input_model = api.model('ProductInput', {
    'name': fields.String,
    'description': fields.String,
    'price': fields.Float,
    'idCategory': fields.Integer
})