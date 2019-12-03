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
        return jsonify(**{'method': 'post'})

    def put(self, id):
        return jsonify(**{'method': 'put'})

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
        return jsonify(**{'method': 'post'})

    def put(self, id=None):
        return jsonify(**{'method': 'put'})

    def delete(self, id):
        Product.objects(id=id).delete()
        return jsonify(**{'product': 'delete'})
