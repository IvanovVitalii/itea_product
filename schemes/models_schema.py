from marshmallow import fields, Schema, ValidationError


class UserSchema(Schema):
    user = fields.String()


class TextsSchema(Schema):
    title = fields.String(max_length=255)
    body = fields.String(max_length=1024)


class PropertiesSchema(Schema):
    weight = fields.Float()


class LazyCatScheme(Schema):
    id = fields.String()
    title = fields.String(max_length=255)
    description = fields.String(max_length=1024)
    parent = fields.Nested('self')


class CategorySchema(Schema):
    id = fields.String()
    title = fields.String(required=True)
    description = fields.String()
    subcategory = fields.List(fields.Nested(LazyCatScheme), load_only=True)
    parent = fields.Nested('self')


class ProductSchema(Schema):
    id = fields.String()
    title = fields.String(max_length=255)
    description = fields.String(max_length=1024)
    price = fields.Integer(min_value=0)
    new_price = fields.Integer(min_value=0)
    is_discount = fields.Bool(default=False)
    logo = fields.String(max_length=255)
    properties = fields.Nested(PropertiesSchema)
    category = fields.Nested(CategorySchema, load_only=True)


class BasketSchema(Schema):
    user = fields.Nested(UserSchema)
    products = fields.Nested(ProductSchema, default=None)


class HistorySchema(Schema):
    user = fields.Nested(UserSchema)
    products = fields.Nested(ProductSchema)
    data = fields.Date()
