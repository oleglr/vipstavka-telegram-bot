from aiogram import Bot, Dispatcher, executor, types
from keyboards import UpdateKeyboard, keyboards, buttons
from config import API_TOKEN, admins, chat_id
import schedule
from multiprocessing.context import Process
import time
import requests
from db_requests import SQLRequests, conn, cursor


r = requests.Session()

#Назначаем переменным клавиатуры
start_keyb = UpdateKeyboard(keyboards, buttons).start_keyboard()
general_admin_keyb = UpdateKeyboard(keyboards, buttons).admin_general_keyboard()

all_users = {}

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)

users_what_pay_access = {}

@dp.message_handler(commands = ['start'])
async def starting (message: types.Message):
    """Функция для вывода информации по команде /start"""
    if message.from_user.id in all_users.keys():
        pass
    else:
        SQLRequests(conn, cursor).write_new_user(message.from_user.id, 
                                                message.from_user.first_name, 
                                                message.from_user.username, 
                                                'Pass', 
                                                'Pass')
        get_all_users_in_start()


    await message.answer("Что бы вы хотели сделать?", reply_markup = start_keyb )

    
@dp.message_handler(lambda message: message.text == "Я оплатил💰")
async def buy_access(message: types.Message):
    """Функция срабатывает при нажатии на кнопку Я оплатил💰"""

    format_message = f"Пользователь {message.from_user.first_name} говорит что оплатил доступ\n\n"\
                     f"ID: {message.from_user.id}\n"\
                     f"Имя: {message.from_user.first_name}\n"\
                     f"@{message.from_user.username}\n\n"\
                     f"Сколько дней выдаем?"
    
    to_admin_keyb = UpdateKeyboard(keyboards, buttons).add_days_button_for_user(str(message.from_user.id))


    await message.answer("Проверяю оплату! Ожидайте...")
    await bot.send_message(366954921, format_message, reply_markup=to_admin_keyb)

@dp.callback_query_handler(lambda c: c.data.startswith("add_days_"))
async def add_days_for_user(c: types.CallbackQuery):
    """Функция для добавления дней пользователю с админ клавиатуры"""
    cut_c_data_for_add_days = c.data.split("_")

    link = await bot.export_chat_invite_link(chat_id=chat_id)

    link_button = UpdateKeyboard(keyboards, buttons).create_invite_link(cut_c_data_for_add_days[2], link)

    await bot.send_message(int(cut_c_data_for_add_days[2]), f"Ваш платеж успешно подтвержден!\n"\
                                                            f"Доступ в закрытый канал открыт на <b>{cut_c_data_for_add_days[3]} дней</b>\n\n"\
                                                            f"{link}"
                                                            ,parse_mode='html', reply_markup=link_button)



@dp.callback_query_handler(lambda c: c.data.startswith("decline_"))
async def decline_days_for_user(c: types.CallbackQuery):
    cut_c_data = c.data.split('_')
    await bot.delete_message(c.from_user.id, c.message.message_id)

    await bot.send_message(int(cut_c_data[1]), "Ваш платеж не подтвержден!")
    
    await bot.send_message(c.from_user.id, f"Отменяем добавление дней для {cut_c_data[1]}")

    


@dp.message_handler(lambda message: message.text == "Связь с оператором📲")
async def communication_with_the_operator(message: types.Message):
    """Функция срабатывает при нажатии на кнопку Связь с оператором📲"""

    await message.answer("Здесь сообщение для связи с оператором")



@dp.message_handler(commands = ['admin'])
async def admin_menu(message: types.Message):
    """Функция срабатывает по команде /admin"""

    if message.from_user.id in admins:
        await message.answer("Вход в админ панель разрешен!\nЧто вы хотите сделать?", reply_markup=general_admin_keyb)


def get_all_users_in_start():
    """Форматируем инфу о пользователях в словарь"""

    users = SQLRequests(conn, cursor).get_users()

    for info in users:
        all_users[info[0]] =     {"ID":info[0], 
                                  "Name":info[1], 
                                  "Username":info[2], 
                                  "Status":info[3],
                                  "Date":info[4]}


if __name__ == "__main__":
    get_all_users_in_start()
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
    	print(e)
