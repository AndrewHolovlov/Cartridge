from bot_object import bot
from database.database import session
from keyboards import *
from database.models import Cartridge, User
from state_handler import get_state_and_process
from enums import State, StateUser
from config import ADMINS


@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        print(State.works)
        user = session.query(User).filter_by(user_id=message.chat.id).first()
        is_admin = False
        if str(message.from_user.id) in ADMINS:
            is_admin = True
        if user is None:
            user = User(
                user_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                state='login_state',
                is_admin=is_admin
            )
            session.add(user)
            session.commit()
        else:
            user.state = 'main_menu_state'
            user.is_admin = is_admin
            session.commit()

        get_state_and_process(message, user, True)
    except Exception as e:
        print(f'Error: {e}')


# @bot.message_handler(content_types=['text'])
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        user = session.query(User).filter_by(user_id=message.chat.id).first()
        if user is None:
            bot.send_message(message.chat.id, 'Ошибка. Для начала введите /start')

        get_state_and_process(message, user)
    except Exception as e:
        print(f'Error: {e}')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # user = session.query(User).filter_by(user_id=call.message.chat.id).first()

    if not call.message:
        bot.delete_message(call.message.chat.id, call.message.message.id)

    if call.data == 'Отмена':
        bot.delete_message(call.message.chat.id, call.message.message_id)

    if call.data.startswith('Да_'):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        id_cartridge = call.data.replace('Да_', '')
        cartridge = session.query(Cartridge).filter_by(id_cartridge=id_cartridge[2:]).first()
        if cartridge is None:
            bot.send_message(call.message.chat.id, 'Error: Произошла ошибка(ДА)')
        else:
            cartridge.state = id_cartridge[:1]
            session.commit()
            bot.send_message(call.message.chat.id, 'Статус картриджа был успешно изменен')

    if call.data.startswith('Нет_'):
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data.startswith(str(State.works.value)):
        id_cartridge = call.data.replace(str(State.works.value) + '_', '')
        cartridge = session.query(Cartridge).filter_by(id_cartridge=id_cartridge).first()
        if cartridge is None:
            bot.send_message(call.message.chat.id, 'Error: Произошла ошибка')
        else:
            if cartridge.state == str(State.fueled.value):
                cartridge.state = str(State.works.value)
                session.commit()
                bot.send_message(call.message.chat.id, 'Картридж был успешно отдан в работу',
                                 reply_markup=get_main_menu())
            elif cartridge.state == str(State.works.value):
                bot.send_message(call.message.chat.id, 'Error: Картридж уже работает\nИзменить статус?',
                                 reply_markup=get_inline_yes_or_not_keyboard(cartridge, State.works.value))
            elif cartridge.state == str(State.refuels.value):
                bot.send_message(call.message.chat.id, 'Error: Картридж сейчас на заправке\nИзменить статус?',
                                 reply_markup=get_inline_yes_or_not_keyboard(cartridge, State.works.value))
            elif cartridge.state == str(State.not_filled.value):
                bot.send_message(call.message.chat.id, 'Error: Картридж не заправлен\nИзменить статус?',
                                 reply_markup=get_inline_yes_or_not_keyboard(cartridge, State.works.value))
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data.startswith(str(State.refuels.value)):
        id_cartridge = call.data.replace(str(State.refuels.value) + '_', '')
        cartridge = session.query(Cartridge).filter_by(id_cartridge=id_cartridge).first()
        if cartridge is None:
            bot.send_message(call.message.chat.id, 'Error: Произошла ошибка')
        else:
            if cartridge.state == str(State.not_filled.value):
                cartridge.state = str(State.refuels.value)
                session.commit()
                bot.send_message(call.message.chat.id, 'Картридж был успешно отдан на заправку',
                                 reply_markup=get_main_menu())
            elif cartridge.state == str(State.works.value):
                bot.send_message(call.message.chat.id,
                                 'Error: Картридж не был сдан в запраку. Сейчас картридж работает\nИзменить статус?',
                                 reply_markup=get_inline_yes_or_not_keyboard(cartridge, State.refuels.value))
            elif cartridge.state == str(State.refuels.value):
                bot.send_message(call.message.chat.id, 'Error: Картридж уже на заправке\nИзменить статус?',
                                 reply_markup=get_inline_yes_or_not_keyboard(cartridge, State.refuels.value))
            elif cartridge.state == str(State.fueled.value):
                bot.send_message(call.message.chat.id, 'Error: Картридж уже заправлен\nИзменить статус?',
                                 reply_markup=get_inline_yes_or_not_keyboard(cartridge, State.refuels.value))
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data.startswith(str(State.not_filled.value)):
        id_cartridge = call.data.replace(str(State.not_filled.value) + '_', '')
        cartridge = session.query(Cartridge).filter_by(id_cartridge=id_cartridge).first()
        if cartridge is None:
            bot.send_message(call.message.chat.id, 'Error: Произошла ошибка')
        else:
            if cartridge.state == str(State.works.value):
                cartridge.state = str(State.not_filled.value)
                session.commit()
                bot.send_message(call.message.chat.id, 'Картридж был успешно принят на заправку',
                                 reply_markup=get_main_menu())
            elif cartridge.state == str(State.refuels.value):
                bot.send_message(call.message.chat.id, 'Error: Картридж сейчас на заправке\nИзменить статус?',
                                 reply_markup=get_inline_yes_or_not_keyboard(cartridge, State.not_filled.value))
            elif cartridge.state == str(State.fueled.value):
                bot.send_message(call.message.chat.id, 'Error: Картридж уже запраленый\nИзменить статус?',
                                 reply_markup=get_inline_yes_or_not_keyboard(cartridge, State.not_filled.value))
            elif cartridge.state == str(State.not_filled.value):
                bot.send_message(call.message.chat.id,
                                 'Error: Картридж уже отдан на склад на запрвку\nИзменить статус?',
                                 reply_markup=get_inline_yes_or_not_keyboard(cartridge, State.not_filled.value))
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data.startswith(str(State.fueled.value)):
        id_cartridge = call.data.replace(str(State.fueled.value) + '_', '')
        cartridge = session.query(Cartridge).filter_by(id_cartridge=id_cartridge).first()
        if cartridge is None:
            bot.send_message(call.message.chat.id, 'Error: Произошла ошибка')
        else:
            if cartridge.state == str(State.refuels.value):
                cartridge.state = str(State.fueled.value)
                session.commit()
                bot.send_message(call.message.chat.id, 'Картридж был успешно принят с заправки',
                                 reply_markup=get_main_menu())
            elif cartridge.state == str(State.works.value):
                bot.send_message(call.message.chat.id, 'Error: Картридж сейчас работает\nИзменить статус?',
                                 reply_markup=get_inline_yes_or_not_keyboard(cartridge, State.fueled.value))
            elif cartridge.state == str(State.fueled.value):
                bot.send_message(call.message.chat.id, 'Error: Картридж уже заправлен\nИзменить статус?',
                                 reply_markup=get_inline_yes_or_not_keyboard(cartridge, State.fueled.value))
            elif cartridge.state == str(State.not_filled.value):
                bot.send_message(call.message.chat.id, 'Error: Картридж на складе не заправлен\nИзменить статус?',
                                 reply_markup=get_inline_yes_or_not_keyboard(cartridge, State.fueled.value))
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data.startswith('status'):
        id_cartridge = call.data.replace('status_', '')
        cartridge = session.query(Cartridge).filter_by(id_cartridge=id_cartridge).first()
        if cartridge is None:
            bot.send_message(call.message.chat.id, 'Error: Произошла ошибка')
        else:
            bot.send_message(call.message.chat.id,
                             f'корпус: {cartridge.corps}\n'+
                             f'тип: {cartridge.types}\n' +
                             f'заметка: {cartridge.note}\n' +
                             f'аудитория: {cartridge.audience}\n'+
                             f'статус: {StateUser[cartridge.state]}\n'+
                             f'дата обновления: {cartridge.last_update}')
    bot.delete_message(call.message.chat.id, call.message.message_id)


if __name__ == '__main__':
    bot.polling(none_stop=True)
