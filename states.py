from bot_object import bot
from database import session
from keyboards import *


def login_state(message, user, is_entry=False):
    if is_entry:
        bot.send_message(message.chat.id, 'Привет, это бот где ты можешь узнать информацию про твой картридж')
    else:
        return True, 'main_menu_state'
    return True, 'main_menu_state'


def main_menu_state(message, user, is_entry=False):
    if is_entry:
        if user.is_admin:
            bot.send_message(message.chat.id, 'Главное меню админа', reply_markup=get_admin_main_menu_keyboard())
        else:
            bot.send_message(message.chat.id, 'Главное меню', reply_markup=get_user_main_menu_keyboard())
    else:
        if user.is_admin:
            if message.text == 'Выдать картридж':
                return True, 'dispense_cartridge'
            elif message.text == 'Взять на заправку':
                return True, 'take_to_refueling'
            elif message.text == 'Принять картридж с заправки':
                return True, 'take_from_refueling'
            elif message.text == 'Отдать картридж на заправку':
                return True, 'give_cartridge_for_refills'
        elif message.text == 'Где мой картридж':
            return True, 'where_is_my_cartridge'

    return False, ''


def dispense_cartridge(message, user, is_entry=False):
    if is_entry:
        bot.send_message(message.chat.id, 'menu: Выдать картридж\nВведите номер:', reply_markup=get_main_menu())
    else:
        if message.text == 'Главное меню':
            return True, 'main_menu_state'
        else:
            pass
    return False, ''


def take_to_refueling(message, user, is_entry=False):
    if is_entry:
        bot.send_message(message.chat.id, 'menu: Взять на заправку\nВведите номер:', reply_markup=get_main_menu())
    else:
        if message.text == 'Главное меню':
            return True, 'main_menu_state'
        else:
            pass
    return False, ''


def take_from_refueling(message, user, is_entry=False):
    if is_entry:
        bot.send_message(message.chat.id, 'menu: Принять картридж с заправки\nВведите номер:',
                         reply_markup=get_main_menu())
    else:
        if message.text == 'Главное меню':
            return True, 'main_menu_state'
        else:
            pass
    return False, ''


def give_cartridge_for_refills(message, user, is_entry=False):
    if is_entry:
        bot.send_message(message.chat.id, 'menu: Отдать картридж на заправку\nВведите номер:',
                         reply_markup=get_main_menu())
    else:
        if message.text == 'Главное меню':
            return True, 'main_menu_state'
        else:
            pass
    return False, ''


def where_is_my_cartridge(message, user, is_entry=False):
    if is_entry:
        bot.send_message(message.chat.id, 'Введите номер:', reply_markup=get_main_menu())
    else:
        if message.text == 'Главное меню':
            return True, 'main_menu_state'
        else:
            pass
    return False, ''