from flask import Flask, request, abort, Response
from schemes.models_schema import *
from models.models import *
from resources.models_resource import *
from flask_restful import Api

app = Flask(__name__)
api = Api(app)


api.add_resource(TextsResource, '/text')
api.add_resource(CategoryResource, '/category', '/category/<string:id>')
api.add_resource(ProductResource, '/product', '/product/<string:id>')


# @app.route('/', methods=['GET', 'POST'])
# def hello_text():
#     if request.method == 'GET':
#         obj = Texts.objects.get()
#         return TextsSchema().dump(obj, many=True)
#     elif request.method == 'POST':
#         Texts(**request.json).save()
#     return Response(status=201)


# @app.route('/category', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def hello_category():
#     if request.method == 'GET':
#         pass
#     elif request.method == 'POST':
#         pass
#     elif request.method == 'PUT':
#         pass
#     elif request.method == 'DELETE':
#         pass
#     LazyCatScheme(**request.json).save()
#     Category(**request.json).save()
#     return Response(status=201)


# @app.route('/product', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def hello_product():
#     if request.method == 'GET':
#         pass
#     elif request.method == 'POST':
#         pass
#     elif request.method == 'PUT':
#         pass
#     elif request.method == 'DELETE':
#         pass
#     Product(**request.json).save()
#     return Response(status=201)


if __name__ == '__main__':
    app.run(debug=True)