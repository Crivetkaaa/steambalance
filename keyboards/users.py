from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class Userskeyboard:
    def start_menu(chat_id):
        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton(
            'Добавить новый аккаунт', callback_data=f'add_new_accaunt:{chat_id}')
        button_1 = InlineKeyboardButton(
            'Посмотреть балансы', callback_data=f'check_balance:{chat_id}')
        keyboard.add(button).add(button_1)
        return keyboard
