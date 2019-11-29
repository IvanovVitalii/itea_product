from flask_restful import Resource
from flask import request, jsonify
from schemes.models_schema import *
from models.models import *


class TextsResource(Resource):

    def get(self):
    return TextsSchema().dump(Texts.objects().get())

    def post(self):
        return jsonify(**{'method': 'post'})

    def put(self, id):
        return jsonify(**{'method': 'put'})

    def delete(self):
        return jsonify(**{'method': 'delete'})


class CategoryResource(Resource):

    def get(self, id=None):
        return jsonify(**{'method': 'get'})

    def post(self):
        return jsonify(**{'method': 'post'})

    def put(self, id):
        return jsonify(**{'method': 'put'})

    def delete(self):
        return jsonify(**{'method': 'delete'})


class ProductResource(Resource):

    def get(self, id=None):
        return jsonify(**{'method': 'get'})

    def post(self):
        return jsonify(**{'method': 'post'})

    def put(self, id):
        return jsonify(**{'method': 'put'})

    def delete(self):
        return jsonify(**{'method': 'delete'})
