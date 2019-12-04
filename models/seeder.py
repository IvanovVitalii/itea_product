from models import *
import random, os

category_list = []
for i in range(5):
    obj = Category(**{'title': f'root {i}',
                      'description': f'descr {i}'}).save()
    obj.add_subcategory(
        Category(**{'title': f' sub {i}',
                 'description': f'descr {i}'})
    )

objects = Category.objects(parent__ne=None)
for i in objects:
    dict_sub_sub = {'title': f'sub-sub {i}',
                    'description': f'd {i}'}
    obj = Category(**dict_sub_sub)
    category_list.append(obj)
    i.add_subcategory(obj)


# with open(os.path.abspath('../logo/logo.jpg'), 'rb') as f:
#     logo = f.read()

for i in range(50):
    price = random.randint(1500, 20000)
    is_discount = bool(random.randint(False, True))
    if is_discount:
        product = {
            'title': f'Продукт-{i}',
            'description': f'Описание-{i}',
            'price': price,
            'new_price': int(price//1.1),
            'is_discount': is_discount,
            'logo': 'logo/logo.jpg',
            'category': random.choice(category_list)
        }
    else:
        product = {
            'title': f'Продукт-{i}',
            'description': f'Описание-{i}',
            'price': price,
            'logo': 'logo/logo.jpg',
            'category': random.choice(category_list)
        }
    Product(**product).save()


# text_dict = {
#     'title': 'Greetings',
#     'body': 'Приветствие'
# }
#
# Texts(**text_dict).save()
