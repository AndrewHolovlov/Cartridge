from bot_object import bot
from database import session
from keyboards import *
from models import Cartridge, User
from state_handler import get_state_and_process


@bot.message_handlers(commands=['start'])
def send_welcom(message):
    try:
        user = session.query(User).filter_by(user_id=message.chat.id).first()
        if user is None:
            user = User(
                user_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                state='login_state',
                is_admin=False
            )
            session.add(user)
            session.commit()
        else:
            user.state = 'main_menu_state'
            session.commit()

        get_state_and_process(message, user, True)
    except Exception as e:
        print(f'Error: {e}')


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        user = session.query(User).filter_by(user_id=message.chat.id).first()
        if user is None:
            bot.send_message(message.chat.id, 'Ошибка. Для начала введите /start')
        else:
            get_state_and_process(message, user)
    except Exception as e:
        print(f'Error: {e}')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user = session.query(User).filter_by(user_id=call.message.chat.id).first()

    if not call.message:
        bot.delete_message(call.message.chat.id, call.message.message.id)

    if call.data == 'Отмена':
        pass


