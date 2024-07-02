from flask import request
from flask_restx import Resource, Namespace
from src.utils.db import db
from src.models.products import Product
from src.models.api_models import product_input_model, product_model, product_model_with_category

ns_product = Namespace('Products')

@ns_product.route('/')
class ProductList(Resource):
    @ns_product.marshal_list_with(product_model_with_category)
    def get(self):
        offset = request.args.get('offset', type=int)
        limit = request.args.get('limit', type=int)
        pricemin = request.args.get('pricemin', type=float)
        pricemax = request.args.get('pricemax', type=float)
        order = request.args.get('order', type=str)

        query = Product.query

        # Filtrar por rango de precios si se especifica
        if pricemin is not None and pricemax is not None:
            query = query.filter(Product.price >= pricemin, Product.price <= pricemax)
        
        # Ordenar los resultados si se especifica
        if order:
            if order.lower() == 'desc':
                query = query.order_by(Product.price.desc())
            elif order.lower() == 'asc':
                query = query.order_by(Product.price.asc())

        # Aplicar paginación si se especifica
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        products = query.all()
        return products, 200

    
    @ns_product.expect(product_input_model)
    @ns_product.marshal_with(product_model_with_category)
    def post(self):
        name = ns_product.payload['name']
        description = ns_product.payload['description']
        price = ns_product.payload['price']
        idCategory = ns_product.payload['idCategory']
        p = Product(name, description, price, idCategory)
        db.session.add(p)
        db.session.commit()
        return p, 201

@ns_product.route('/<int:id>')
class ProductOne(Resource):
    @ns_product.marshal_with(product_model_with_category)
    def get(self, id):
        return Product.query.filter_by(id=id).first(), 200
    
    @ns_product.expect(product_input_model)
    @ns_product.marshal_with(product_model_with_category)
    def put(self, id):
        p = Product.query.filter_by(id=id).first()
        p.name = ns_product.payload['name']
        p.description = ns_product.payload['description']
        p.price = ns_product.payload['price']
        p.idCategory = ns_product.payload['idCategory']
        db.session.commit()
        return p, 200
    
    def delete(self, id):
        p = Product.query.filter_by(id=id).first()
        db.session.delete(p)
        db.session.commit()
        return {}, 204