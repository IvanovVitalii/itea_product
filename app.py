# интернет магазин бот + rest
import telebot
import keyboards
import config
import datetime
import os
from keyboards import *
from flask import Flask, request, abort
from models.models import *

app = Flask(__name__)
bot = telebot.TeleBot(config.TOKEN)

# Process webhook calls
@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)


@bot.message_handler(commands=['start'])
def start(message):
    '''

    :param message:
    :return: home page
    '''
    try:
        user = User.objects(user=str(message.chat.id)).get().user
        print('user found')
    except:
        user = User(**{'user': f'{message.chat.id}'}).save()
        Basket(**{'user': user, 'products': []}).save()
        print('user add')
    greetings_str = 'Магазин-Телеграм BOT'
    kb = InlineKeyboardMarkup()
    button = []
    keyboard = keyboards.beginning_kb
    for i in keyboard.keys():
        button.append(InlineKeyboardButton(text=f'{keyboard.get(i)}',
                                           callback_data=f'{i}_0'))
    kb.add(*button)
    bot.send_message(message.chat.id, greetings_str, reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'news')
def show_categories(call):
    '''

    :param message:
    :return: listed root category
    '''
    kb = InlineKeyboardMarkup()
    button = [InlineKeyboardButton(text=f'На главную',
                                   callback_data=f'home_/start')]
    kb.add(*button)
    text = 'Новостей нет'
    bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'products')
def show_categories(call):
    '''

    :param message:
    :return: listed root category
    '''
    kb = keyboards.InlineKB(
        key='root',
        lookup_field='id',
        named_arg='category'
    )
    kb.generate_kb()
    kb.add(InlineKeyboardButton(text='<<',
                                callback_data='home_/start'))
    bot.edit_message_text(text='Выберите категорию', chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'about')
def show_categories(call):
    '''

    :param call:
    :return: about store
    '''
    kb = InlineKeyboardMarkup()
    button = [InlineKeyboardButton(text=f'На главную',
                                   callback_data=f'home_/start')]
    kb.add(*button)
    text = Texts.objects(title='Greetings').get().body
    bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'sales')
def show_sales_product(call):
    '''

    :param call:
    :return: discount products
    '''
    product = Product.objects(is_discount=True).all()
    kb = keyboards.InlineKB(
        iterable=product,
        lookup_field='id',
        named_arg='product'
    )
    kb.generate_kb()
    kb.add(InlineKeyboardButton(text=f'<<',
                                callback_data=f'home_0'))
    try:
        bot.edit_message_text(text='Товары со скидкой', chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=kb)
    except:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(text='Товары со скидкой', chat_id=call.message.chat.id,
                         reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'category')
def show_products_or_sub_category(call):
    '''

    :param call:
    :return: listed subcategory || listed products
    '''
    obj_id = call.data.split('_')[1]
    category = Category.objects(id=obj_id).get()
    if category.is_parent:
        kb = keyboards.InlineKB(
            iterable=category.subcategory,
            lookup_field='id',
            named_arg='category'
        )
        kb.generate_kb()
        kb.add(InlineKeyboardButton(text='<<',
                                    callback_data=f'back_{category.id}'))
        bot.edit_message_text(text=category.title, chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=kb)
    else:
        product = Product.objects(category=obj_id, is_discount=False).all()
        kb = keyboards.InlineKB(
            iterable=product,
            lookup_field='id',
            named_arg='product'
        )
        kb.generate_kb()
        kb.add(InlineKeyboardButton(text=f'<<',
                                    callback_data=f'back_{category.id}'))
        bot.edit_message_text(text=category.title, chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'product')
def show_product(call):
    '''

    :param call:
    :return: product page
    '''
    obj_id = call.data.split('_')[1]
    product = Product.objects(id=obj_id).get()
    category = Category.objects(id=product.category.id).get()

    if product.is_discount:
        description = f'{product.title}\n{product.description}\nЦена без скидки: {int(product.price) / 100}\n' \
                      f'Цена со скидкой: <b>{int(product.new_price) / 100}</b>'
        kb = InlineKeyboardMarkup()
        button = [
            InlineKeyboardButton(text='В корзину',
                                 callback_data=f'buy_{product.id}'),
            InlineKeyboardButton(text=f'<<',
                                 callback_data='sales_0')
        ]
    else:
        description = f'{product.title}\n{product.description}\nЦена: <b>{int(product.price) / 100}</b>'
        kb = InlineKeyboardMarkup()
        button = [
            InlineKeyboardButton(text='В корзину',
                                 callback_data=f'buy_{product.id}'),
            InlineKeyboardButton(text=f'<<',
                                 callback_data=f'back_{category.id}')
        ]

    with open(os.path.abspath(product.logo), 'rb') as f:
        logo = f.read()
    kb.add(*button)
    bot.send_photo(chat_id=call.message.chat.id, photo=logo,
                   caption=description, reply_markup=kb, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'buy')
def add_to_basket(call):
    '''

    :param call:
    :return: product in basket
    '''
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    obj_id = call.data.split('_')[1]
    product = Product.objects(id=obj_id)
    user = User.objects(user=str(call.message.chat.id)).get()
    category = Category.objects(id=product.get().category.id).get()
    basket = Basket.objects(user=user.id).get()
    basket.update(push__products=product.get())
    kb = InlineKeyboardMarkup()
    button = [
        InlineKeyboardButton(text=f'Корзина',
                             callback_data=f'basket_0'),
        InlineKeyboardButton(text=f'<<',
                             callback_data=f'back_{category.id}')
    ]
    kb.add(*button)

    bot.send_message(text='Товар в корзине',
                          chat_id=call.message.chat.id, reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'basket')
def basket(call):
    '''

    :param call:
    :return: basket page
    '''
    user = User.objects(user=str(call.message.chat.id)).get()

    if call.data.split('_')[1] == '0':
        basket = Basket.objects(user=user)
    else:
        delete_product = Product.objects(id=call.data.split('_')[1])
        basket_old = Basket.objects(user=user)
        basket_old.update(pull__products=delete_product.get())
        basket = Basket.objects(user=user)
    sum = 0
    button = []
    kb = InlineKeyboardMarkup(row_width=1)
    for i in basket:
        for product in i.products:
            if not product.is_discount:
                price_text = f'Цена: {int(product.price) / 100}'
                sum += product.price / 100
            else:
                price_text = f'Цена со скидкой:{int(product.new_price) / 100}'
                sum += product.new_price / 100
            button.append(
                InlineKeyboardButton(text=f'{product.title}\n{price_text}\nУдалить?',
                                     callback_data=f'basket_{product.id}')
            )
    buttons = (
        InlineKeyboardButton(text=f'Оплатить: {sum}',
                             callback_data=f'pay_0'),
        InlineKeyboardButton(text=f'<<',
                             callback_data=f'home_/start')
    )
    kb.add(*button)
    kb.add(*buttons)

    bot.send_message(text=f'К оплате: <b>{sum}</b> \nТовары в корзине:',
                     chat_id=call.message.chat.id, reply_markup=kb, parse_mode='HTML')
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'pay')
def pay(call):
    '''

    :param call:
    :return: payment
    '''
    user = User.objects(user=str(call.message.chat.id)).get()
    basket = Basket.objects(user=user).get()
    products = basket.products
    data = datetime.datetime.now()
    History(**{'user': user,
               'products': products,
               'data': data}).save()
    Basket.objects(user=user).update(pull_all__products=products)
    kb = InlineKeyboardMarkup()
    button = [InlineKeyboardButton(text=f'На главную',
                                  callback_data=f'home_/start')]
    kb.add(*button)
    bot.edit_message_text(text='Спасибо за покупку', chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'back')
def go_back(call):
    '''

    :param call:
    :return: go back
    '''
    obj_id = call.data.split('_')[1]
    category = Category.objects(id=obj_id).get()
    if category.is_root:

        kb = keyboards.InlineKB(
            key='root',
            lookup_field='id',
            named_arg='category'
        )
        kb.generate_kb()
        kb.add(InlineKeyboardButton(text='<<',
                                    callback_data='home_/start'))
    else:

        kb = keyboards.InlineKB(
            iterable=category.parent.subcategory,
            lookup_field='id',
            named_arg='category'
        )
        kb.generate_kb()
        kb.add(InlineKeyboardButton(text=f'<<',
                                    callback_data=f'back_{category.parent.id}'))
    text = 'Выберите категорию' if not category.parent else category.parent.title
    try:
        bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=kb)
    except:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'home')
def home(call):
    '''

    :param call:
    :return: go back to home page
    '''
    try:
        user = User.objects(user=str(call.message.chat.id)).get().user
    except:
        user = User(**{'user': f'{call.message.chat.id}'}).save()
        Basket(**{'user': user}).save()
    greetings_str = 'Магазин-Телеграм BOT'
    kb = InlineKeyboardMarkup()
    button = []
    keyboard = keyboards.beginning_kb
    for i in keyboard.keys():
        button.append(InlineKeyboardButton(text=f'{keyboard.get(i)}',
                                           callback_data=f'{i}_0'))
    kb.add(*button)
    bot.edit_message_text(text=greetings_str, chat_id=call.message.chat.id,
                          message_id=call.message.message_id,  reply_markup=kb)


if __name__ == '__main__':
    import time
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(config.webhook_url,
                       certificate=open('webhook_cert.pem', 'r'))
    app.run(debug=True)
    bot.polling(none_stop=True)
