from marshmallow import fields, Schema


class UserSchema(Schema):
    user = fields.String()


class TextsSchema(Schema):
    title = fields.String()
    body = fields.String()


class PropertiesSchema(Schema):
    weight = fields.Float()


class LazyCatScheme(Schema):

    id = fields.String()
    title = fields.String()
    description = fields.String()
    parent = fields.Nested('self')


class CategorySchema(LazyCatScheme):
    subcategory = fields.List(fields.Nested(LazyCatScheme))


class ProductSchema(Schema):
    title = fields.String(max_length=255)
    description = fields.String(max_length=1024)
    price = fields.Integer(min_value=0)
    new_price = fields.Integer(min_value=0)
    is_discount = fields.Boolean(default=False)
    logo = fields.FieldABC()
    properties = fields.Nested(PropertiesSchema)
    category = fields.Nested(CategorySchema)


class BasketSchema(Schema):
    user = fields.Nested(UserSchema)
    products = fields.Nested(ProductSchema, default=None)


class HistorySchema(Schema):
    user = fields.Nested(UserSchema)
    products = fields.Nested(ProductSchema)
    data = fields.Date()
