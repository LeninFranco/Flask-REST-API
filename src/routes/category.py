from flask_restx import Resource, Namespace
from src.utils.db import db
from src.models.categories import Category
from src.models.api_models import category_model, category_input_model

ns_category = Namespace('Categories')

@ns_category.route('/')
class CategoryList(Resource):
    @ns_category.marshal_list_with(category_model)
    def get(self):
        return Category.query.all(), 200
    
    @ns_category.expect(category_input_model)
    @ns_category.marshal_with(category_model)
    def post(self):
        name = ns_category.payload['name']
        c = Category(name)
        db.session.add(c)
        db.session.commit()
        return c, 201

@ns_category.route('/<int:id>')
class CategoryOne(Resource):
    @ns_category.marshal_with(category_model)
    def get(self, id):
        return Category.query.filter_by(id=id).first(), 200
    
    @ns_category.expect(category_input_model)
    @ns_category.marshal_with(category_model)
    def put(self, id):
        c = Category.query.filter_by(id=id).first()
        c.name = ns_category.payload['name']
        db.session.commit()
        return c, 200

    def delete(self, id):
        c = Category.query.filter_by(id=id).first()
        db.session.delete(c)
        db.session.commit()
        return {}, 204