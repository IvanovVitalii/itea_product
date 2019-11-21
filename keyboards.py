from telebot.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton
)
from models.models import (
    Texts,
    Properties,
    Category,
    Product,
)

beginning_kb = {
    'news': 'Последние новости',
    'products': 'Продукты',
    'sales': 'Товар со скидкой',
    'about': 'Информация о магазине',
    'basket': 'Корзина'
}


category = Category.objects()
category_kb = []
for i in category:
    category_kb.append(i.title)


class ReplyKB(ReplyKeyboardMarkup):
    def __init__(self, one_time_keyboard=True, resize_keyboard=True, row_width=3):
        super().__init__(one_time_keyboard=one_time_keyboard,
                         resize_keyboard=resize_keyboard,
                         row_width=row_width)

    def generate_kb(self, *args):
        '''
        :param args: Button names
        :return: New kb
        '''
        buttons = [KeyboardButton(x) for x in args]
        self.add(*buttons)
        return self


class InlineKB(InlineKeyboardMarkup):

    queries = {
        'root': Category.get_root_categories()
    }

    def __init__(self,  named_arg, iterable=None, lookup_field='id', key=None, title_field='title', row_width=3):
        if all([iterable, key]):
            raise ValueError('Only one of fields: iterable, key can be set')
        super().__init__(row_width=row_width)
        self._iterable = iterable
        self._named_arg = named_arg
        self._lookup_field = lookup_field
        self._title_field = title_field
        self._query = self.queries.get(key)

    def generate_kb(self):
        buttons = []

        if not self._iterable:
            self._iterable = self._query
        for i in self._iterable:
            buttons.append(InlineKeyboardButton(
                text=str(getattr(i, self._title_field)),
                callback_data=f'{self._named_arg}_' + str(getattr(i, self._lookup_field))
            ))

        self.add(*buttons)
        return self
