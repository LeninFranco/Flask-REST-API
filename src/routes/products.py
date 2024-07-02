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
        offset = request.args.get('offset')
        limit = request.args.get('limit')
        pricemin = request.args.get('pricemin')
        pricemax = request.args.get('pricemax')
        orderA = request.args.get('orderA')
        orderD = request.args.get('orderD')
        if offset is None and limit is None and pricemin is None and pricemax is None and orderA is None and orderD is None:
            products = Product.query.all()
        else:
            orderA = True if orderA == 'true' else False
            orderD = True if orderD == 'true' else False
            if offset is None and limit is None and pricemin is None and pricemax is None:
                if orderA is None:
                    products = Product.query.order_by(Product.price.desc()).all()
                else:
                    products = Product.query.order_by(Product.price.asc()).all()
            elif pricemax is None and pricemin is None:
                offset = int(offset)
                limit = int(limit)
                if orderA is None:
                    products = Product.query.order_by(Product.price.desc()).offset(offset).limit(limit).all()
                else:
                    products = Product.query.order_by(Product.price.asc()).offset(offset).limit(limit).all()
            elif offset is None and limit is None:
                pricemin = float(pricemin)
                pricemax = float(pricemax)
                if orderA is None:
                    products = Product.query.filter(Product.price >= pricemin, Product.price <= pricemax).order_by(Product.price.desc()).all()
                else:
                    products = Product.query.filter(Product.price >= pricemin, Product.price <= pricemax).order_by(Product.price.asc()).all()
            else:
                pricemin = float(pricemin)
                pricemax = float(pricemax)
                limit = int(limit)
                if orderA is None:
                    products = Product.query.filter(Product.price >= pricemin, Product.price <= pricemax).order_by(Product.price.desc()).limit(limit).all()
                else:
                    products = Product.query.filter(Product.price >= pricemin, Product.price <= pricemax).order_by(Product.price.asc()).limit(limit).all()
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