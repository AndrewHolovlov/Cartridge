from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


def get_user_main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Где мой картридж')
    return keyboard


def get_admin_main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Выдать картридж')
    keyboard.add('Взять на заправку')
    keyboard.add('Принять картридж с заправки')
    keyboard.add('Отдать картридж на заправку')
    keyboard.add('Где мой картридж')
    return keyboard


def get_main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Главное меню')
    return keyboard


def get_inline_cartridge_keyboard(cartridges, state):
    keyboard = InlineKeyboardMarkup()

    buttons = []
    for cartridge in cartridges:
        buttons.append(InlineKeyboardButton(
            f'{cartridge.id_cartridge} {cartridge.types}',
            callback_data=f'{state}_{cartridge.id_cartridge}')
        )

    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton('Отмена', callback_data='Отмена'))
    return keyboard


def get_inline_yes_or_not_keyboard(cartridge, state):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Да', callback_data=f'Да_{state}_{cartridge.id_cartridge}'))
    keyboard.add(InlineKeyboardButton('Нет', callback_data=f'Нет_{state}_{cartridge.id_cartridge}'))
    return keyboard
