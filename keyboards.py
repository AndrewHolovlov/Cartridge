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
    keyboard.add('Где мой картридж')
    return keyboard


def get_main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Главное меню')
    return keyboard
