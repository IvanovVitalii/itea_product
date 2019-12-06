from flask import Flask
from resources.models_resource import *
from flask_restful import Api

app = Flask(__name__)
api = Api(app)


api.add_resource(TextsResource, '/text')
api.add_resource(CategoryResource, '/category', '/category/<string:id>')
api.add_resource(ProductResource, '/product', '/product/<string:id>')
api.add_resource(HistoryResourse, '/history', '/history/<string:id>')


if __name__ == '__main__':
    app.run(debug=True)
