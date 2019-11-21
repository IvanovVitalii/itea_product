from mongoengine import *

connect('wep_shop_bot')


class User(Document):
    user = StringField(max_length=255)


class Texts(Document):
    title = StringField(unique=True)
    body = StringField(max_length=4096)


class Properties(DynamicEmbeddedDocument):
    weight = FloatField(min_value=0)


class Category(Document):
    title = StringField(max_length=255, required=True)
    description = StringField(max_length=512)
    subcategory = ListField(ReferenceField('self'))
    parent = ReferenceField('self')

    @classmethod
    def get_root_categories(cls):
        return cls.objects(parent=None)

    @property
    def is_root(self):
        return not bool(self.parent)

    @property
    def is_parent(self):
        return bool(self.subcategory)

    @property
    def get_products(self, **kwargs):
        return Product.objects(category=self, **kwargs)

    def add_subcategory(self, obj):
        obj.parent = self
        obj.save()
        self.subcategory.append(obj)
        self.save()


class Product(Document):
    title = StringField(max_length=255)
    description = StringField(max_length=1024)
    price = IntField(min_value=0)
    new_price = IntField(min_value=0)
    is_discount = BooleanField(default=False)
    logo = BinaryField(default=None)
    properties = EmbeddedDocumentField(Properties)
    category = ReferenceField(Category)
    # tag

    @property
    def get_price(self):
        if self.is_discount:
            return str(self.new_price / 100)
        return str(self.price / 100)

    @classmethod
    def get_discount_products(cls, **kwargs):
        return cls.objects(is_discount=True, **kwargs)


class Basket(Document):
    user = ReferenceField(User)
    products = ListField(ReferenceField(Product), default=None)


class History(Document):
    user = ReferenceField(User)
    products = ListField(ReferenceField(Product))
    data = DateField()


# History.objects.delete()
# Basket.objects.delete()
# User.objects.delete()
# Product.objects.delete()
# Category.objects.delete()
# Texts.objects.delete()
