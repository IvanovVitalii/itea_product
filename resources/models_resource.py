from flask_restful import Resource
from flask import request, jsonify
from schemes.models_schema import *
from models.models import *


class TextsResource(Resource):

    def get(self):
        return TextsSchema().dump(Texts.objects().get())

    def post(self):
        obj = Texts(**request.json).save()
        return TextsSchema().dump(Texts.objects(id=obj.id).get())

    def put(self):
        obj = Texts.objects().get()
        obj.update(**request.json)
        return TextsSchema().dump(obj.reload())

    def delete(self):
        Texts.objects().delete()
        return jsonify(**{'object': 'delete'})


class CategoryResource(Resource):

    def get(self, id=None):
        if not id:
            objects = Category.objects
            return CategorySchema().dump(objects, many=True)
        return CategorySchema().dump(Category.objects(id=id).get())

    def post(self):
        obj = Category(**request.json).save()
        return CategorySchema().dump(Category.objects(id=obj.id).get())

    def put(self, id):
        obj = Category.objects(id=id).get()
        obj.update(**request.json)
        return CategorySchema().dump(obj.reload())

    def delete(self, id):
        Category.objects(id=id).delete()
        return jsonify(**{'category': 'delete'})


class ProductResource(Resource):

    def get(self, id=None):
        if not id:
            objects = Product.objects
            return ProductSchema().dump(objects, many=True)
        return ProductSchema().dump(Product.objects(id=id).get())

    def post(self):
        obj = Product(**request.json).save()
        return ProductSchema().dump(Category.objects(id=obj.id).get())

    def put(self, id):
        obj = Product.objects(id=id).get()
        obj.update(**request.json)
        return ProductSchema().dump(obj.reload())

    def delete(self, id):
        Product.objects(id=id).delete()
        return jsonify(**{'product': 'delete'})


class HistoryResourse(Resource):

    def get(self, user_id=None):
        if not user_id:
            return HistorySchema().dump(History.objects(), many=True)
        return HistorySchema().dump(History.objects(user=user_id).get())