from aiogram import types
from aiogram.dispatcher import Dispatcher
from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from keyboards.users import Userskeyboard
from aiogram.dispatcher.filters.state import State, StatesGroup
from utils.selen import Selen
from utils.parse import BalanceChecker
from config import Config
import datetime
import os


class FSMSteaminfo(StatesGroup):
    steam_login = State()
    steam_password = State()


class User:
    def __init__(self, user_id):
        Global.users[user_id] = self
        self.user_id = user_id
        self.all_message = []

    async def send_message(self, msg, keyboard=None):
        message = await bot.send_message(chat_id=self.user_id, text=msg, reply_markup=keyboard)
        self.all_message.append(message.message_id)

    async def edit_mesasge(self, msg, keyboard=None):
        text_message = await self.generate_update(msg)
        try:
            await bot.edit_message_text(chat_id=self.user_id, message_id=self.all_message[-1], text=text_message, reply_markup=keyboard)
        except:
            pass

    async def generate_update(self, msg):
        msg += f'\n{datetime.datetime.now()}'
        return msg


class Global:
    users = dict()

    @classmethod
    async def get_user_by_id(cls, user_id) -> User:
        if user_id in cls.users:
            return cls.users[user_id]
        else:
            usr = User(user_id)
            return usr


@dp.callback_query_handler()
async def callback(callback, state: FSMContext):
    segs = callback.data.split(':')
    usr = await Global.get_user_by_id(int(segs[-1]))
    if segs[0] == 'check_balance':
        if not os.path.exists('files/account.txt'):
            await usr.edit_mesasge('Аккаунты ещё не были добавленны', Userskeyboard.start_menu(usr.user_id))
        else:
            with open("files/account.txt", 'r') as file:
                account_data = file.readlines()
            message = ''
            for accaunt in account_data:
                login, password = accaunt.split(':')
                balance = await BalanceChecker.get_balance(str(login))
                message += f'{login}:{balance}\n'
            await usr.edit_mesasge(message, Userskeyboard.start_menu(usr.user_id))

    elif segs[0] == 'add_new_accaunt':
        await usr.send_message('Отправте логин от стима')
        await FSMSteaminfo.steam_login.set()
    await callback.answer()


async def get_login(msg: types.Message, state: FSMContext):
    usr = await Global.get_user_by_id(msg.from_user.id)
    async with state.proxy() as data:
        data['login'] = msg.text
    await FSMSteaminfo.next()
    await usr.send_message('Отправте пароль')


async def get_password(msg: types.Message, state: FSMContext):
    usr = await Global.get_user_by_id(msg.from_user.id)
    async with state.proxy() as data:
        login = data['login']
        password = msg.text
    await state.finish()
    check_accaunt = await Selen.check_accunt(login, password)
    if check_accaunt:
        await usr.send_message('Аккаунт добавлен', Userskeyboard.start_menu(usr.user_id))
        with open('files/account.txt', 'a', encoding='UTF-8') as file:
            file.write(f"{login}:{password}\n")
    else:
        await usr.send_message("Неверный логин или пароль", Userskeyboard.start_menu(usr.user_id))


async def start(msg: types.Message):
    if msg.from_user.id in Config.admins:
        usr = await Global.get_user_by_id(msg.from_user.id)
        await usr.send_message('start menu', Userskeyboard.start_menu(usr.user_id))


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(
        get_login, state=FSMSteaminfo.steam_login, content_types=['text'])
    dp.register_message_handler(
        get_password, state=FSMSteaminfo.steam_password, content_types=['text'])
