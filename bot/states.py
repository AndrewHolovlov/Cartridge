from requests import request

from bot.bot_object import bot
from database.database import session
from database.models import Cartridge
from bot.keyboards import *
from bot.enums import State


def login_state(message, user=None, is_entry=False):
    bot.send_message(message.chat.id, 'Привет, это бот где ты можешь узнать информацию про твой картридж')
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
        if message.text == 'Где мой картридж':
            return True, 'where_is_my_cartridge'

    return False, ''


def dispense_cartridge(message, user, is_entry=False):
    if is_entry:
        bot.send_message(message.chat.id, 'menu: Выдать картридж\nВведите номер:', reply_markup=get_main_menu())
    else:
        if message.text == 'Главное меню':
            return True, 'main_menu_state'
        else:
            cartridges = session.query(Cartridge).filter_by(id_cartridge=message.text).all()
            if len(cartridges) == 0:
                bot.send_message(message.chat.id, 'Такого картриджа нет в базе')
            else:
                bot.send_message(message.chat.id, 'Выберете из списка',
                                 reply_markup=get_inline_cartridge_keyboard(cartridges, State.works.value))
    return False, ''


def take_to_refueling(message, user, is_entry=False):
    if is_entry:
        bot.send_message(message.chat.id, 'menu: Взять на заправку\nВведите номер:', reply_markup=get_main_menu())
    else:
        if message.text == 'Главное меню':
            return True, 'main_menu_state'
        else:
            cartridges = session.query(Cartridge).filter_by(id_cartridge=message.text).all()
            if len(cartridges) == 0:
                bot.send_message(message.chat.id, 'Такого картриджа нет в базе')
            else:
                bot.send_message(message.chat.id, 'Выберете из списка',
                                 reply_markup=get_inline_cartridge_keyboard(cartridges, State.not_filled.value))
    return False, ''


def take_from_refueling(message, user, is_entry=False):
    if is_entry:
        bot.send_message(message.chat.id, 'menu: Принять картридж с заправки\nВведите номер:',
                         reply_markup=get_main_menu())
    else:
        if message.text == 'Главное меню':
            return True, 'main_menu_state'
        else:
            cartridges = session.query(Cartridge).filter_by(id_cartridge=message.text).all()
            if len(cartridges) == 0:
                bot.send_message(message.chat.id, 'Такого картриджа нет в базе')
            else:
                bot.send_message(message.chat.id, 'Выберете из списка',
                                 reply_markup=get_inline_cartridge_keyboard(cartridges, State.fueled.value))
    return False, ''


def give_cartridge_for_refills(message, user, is_entry=False):
    if is_entry:
        bot.send_message(message.chat.id, 'menu: Отдать картридж на заправку\nВведите номер:',
                         reply_markup=get_main_menu())
    else:
        if message.text == 'Главное меню':
            return True, 'main_menu_state'
        else:
            cartridges = session.query(Cartridge).filter_by(id_cartridge=message.text).all()
            if len(cartridges) == 0:
                bot.send_message(message.chat.id, 'Такого картриджа нет в базе')
            else:
                bot.send_message(message.chat.id, 'Выберете из списка',
                                 reply_markup=get_inline_cartridge_keyboard(cartridges, State.refuels.value))
    return False, ''


def where_is_my_cartridge(message, user, is_entry=False):
    if is_entry:
        bot.send_message(message.chat.id, 'Введите номер:', reply_markup=get_main_menu())
    else:
        if message.text == 'Главное меню':
            return True, 'main_menu_state'
        else:
            cartridges = session.query(Cartridge).filter(Cartridge.id_cartridge.like(f'%{message.text}%')).all()
            if len(cartridges) == 0:
                bot.send_message(message.chat.id, 'Такого картриджа нет в базе')
            else:
                bot.send_message(message.chat.id, 'Выберете из списка',
                                 reply_markup=get_inline_cartridge_keyboard(cartridges, 'status'))
    return False, ''
