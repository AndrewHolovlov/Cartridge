from database.database import session
from database.models import User
from states import *


states = {
    'login_state': login_state,
    'main_menu_state': main_menu_state,
    'dispense_cartridge': dispense_cartridge,
    'take_to_refueling': take_to_refueling,
    'take_from_refueling': take_from_refueling,
    'give_cartridge_for_refills': give_cartridge_for_refills,
    'where_is_my_cartridge': where_is_my_cartridge,
}


def get_state_and_process(message, user: User, is_entry=False):
    if user.state in states:
        change_state, state_to_change_name = states[user.state](message, user, is_entry)
    else:
        user.state = 'main_menu_state'
        session.commit()
        change_state, state_to_change_name = states[user.state](message, user, is_entry)
    if change_state:
        go_to_state(message, state_to_change_name, user)


def go_to_state(message, state_name: str, user: User):
    user.state = state_name
    session.commit()
    get_state_and_process(message, user, is_entry=True)
