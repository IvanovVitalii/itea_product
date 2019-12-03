from marshmallow import fields, Schema, ValidationError


class BytesField(fields.Field):
    def _validate(self, value):
        if not isinstance(value, bytes):
            raise ValidationError('Invalid input type.')

        if value is None or value == b'':
            raise ValidationError('Invalid value')


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


class CategorySchema(Schema):
    id = fields.String()
    title = fields.String(required=True)
    description = fields.String()
    subcategory = fields.List(fields.Nested(LazyCatScheme), load_only=True)
    parent = fields.Nested('self', load_only=True)


class ProductSchema(Schema):
    title = fields.String(max_length=255)
    description = fields.String(max_length=1024)
    price = fields.Integer(min_value=0)
    new_price = fields.Integer(min_value=0)
    is_discount = fields.Bool(default=False)
    logo = BytesField(required=True)
    properties = fields.Nested(PropertiesSchema)
    category = fields.Nested(CategorySchema, load_only=True)


class BasketSchema(Schema):
    user = fields.Nested(UserSchema)
    products = fields.Nested(ProductSchema, default=None)


class HistorySchema(Schema):
    user = fields.Nested(UserSchema)
    products = fields.Nested(ProductSchema)
    data = fields.Date()
