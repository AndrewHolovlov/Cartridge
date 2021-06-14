import enum


class State(enum.Enum):
    works = 1
    refuels = 2
    fueled = 3
    not_filled = 4


StateUser = {
    '1': 'работает',
    '2': 'на заправке',
    '4': 'отдан на заправку',
    '3': 'заправлен, заберите',
}


