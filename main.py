from aiogram import Bot, Dispatcher, executor, types
from keyboards import UpdateKeyboard, keyboards, buttons
from config import API_TOKEN, admins, chat_id
import schedule
from multiprocessing.context import Process
import time
import requests
from db_requests import SQLRequests, conn, cursor
import datetime

today = datetime.datetime.today()
now = today.strftime("%Y-%m-%d-%H.%M")


r = requests.Session()
logs = {}

MALLING_STATUS = False


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
    global today, now

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


@dp.message_handler(lambda message: message.text == "Приобрести доступ🔐")
async def why_but_access(message: types.Message):
    
    await message.answer("Оплату можно произвести по реквизитам ниже:\n\nНомер Карты:\n4890494693625188\n\n"\
                        "💳 Онлайн оплата с карты:\nhttp://bit.ly/to_card\n\n"\
                        "📱 Qiwi: +79061007766\n💵 Яндекс Деньги: 410011650372076\n\n"\
                        "(можно со сберонлайн:  Платежи > Остальное > в поиске ввести яндекс деньги)\n\n"\
                        "⚠️После оплаты присылай скриншот менеджеру в лс @bet_market\n\n"\
                        "Нажми кнопку «Я оплатил/продлил💰» ниже. \nПроверю и выдам доступ.")



@dp.message_handler(lambda message: message.text == "Я оплатил/продлил💰")
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

    user_Id = str(cut_c_data_for_add_days[2])
    name = all_users[int(cut_c_data_for_add_days[2])]["Name"]
    username = all_users[int(cut_c_data_for_add_days[2])]["Username"]
    action = "Выдан доступ для: "
    
    SQLRequests(conn, cursor).add_action(now, action, user_Id, name, username)

    await bot.send_message(int(cut_c_data_for_add_days[2]), f"Ваш платеж успешно подтвержден!\n"\
                                                            f"Доступ в закрытый канал открыт на <b>{cut_c_data_for_add_days[3]} дней</b>\n\n"\
                                                            f"{link}"
                                                            ,parse_mode='html', reply_markup=link_button)


@dp.callback_query_handler(lambda c: c.data in ["new_malling",
                                                "action_history",
                                                "add_all_1_day"])

async def react_admin_general_button(message:types.Message):
    """Работаем с главной админ клавиатурой"""
    global MALLING_STATUS

    if c.from_user.id in admins:

        """Создание рассылки"""

        if c.data == "new_malling"
            MALLING_STATUS = True
            admin_buttons = UpdateKeyboard(keyboards, buttons).add_admin_buttons("Malling")
            await message.answer("Перехожу в режим ожидания сообщения для рассылки\n\n"
                                "Примечание: <b>Сообщение не может содержать более 1024 символов!</b>"
                                parse_mode='html')
        
        elif c.data == "new_malling" and MALLING_STATUS == True:
            await message.answer("Я уже ожидаю сообщение для рассылки...")
    

        """Сортировка истории действий"""
        if c.data == "action_history":
            admin_buttons = UpdateKeyboard(keyboards, buttons).add_admin_buttons("History")

            await message.answer("За какой период смотрим историю?", reply_markup=admin_buttons)
        

        """Добавлением всем активным +1 день к доступу в канал"""
        if c.data == "add_all_1_day":
            admin_buttons = UpdateKeyboard(keyboards, buttons).add_admin_buttons("Add_All_1_Day")

            await message.answer("Подтвердить добавление всем активным пользователям +1 день доступ в канал?", reply_markup=admin_buttons)



    

@dp.callback_query_handler(lambda c: c.data in ["access_malling", 
                                                "decline_malling",
                                                "view_history_1", 
                                                "view_history_7", 
                                                "view_history_30",
                                                "access_add_all_one_day",
                                                "decline_add_all_one_day"])

async def admin_access_and_sort_buttons(c: types.CallbackQuery):
    """Работа с кнопками для сортировки или подтверждения/отменения админ действий"""


    """Подтвердить/отменить рассылку"""
    if c.data == "access_malling":
        await message.answer("Рассылка успешно запущена!")
    elif c.data == "decline_malling":
        MALLING_STATUS = False
        await message.answer("Рассылка отменена")



@dp.message_handler(content_types = ['text'])
async def get_text_for_malling(message: types.Message)





@dp.callback_query_handler(lambda c: c.data.startswith("decline_"))
async def decline_days_for_user(c: types.CallbackQuery):
    cut_c_data = c.data.split('_')
    await bot.delete_message(c.from_user.id, c.message.message_id)

    await bot.send_message(int(cut_c_data[1]), "Ваш платеж не подтвержден!")
    
    await bot.send_message(c.from_user.id, f"Отменяем добавление дней для {cut_c_data[1]}")

    


@dp.message_handler(lambda message: message.text == "Связь с оператором📲")
async def communication_with_the_operator(message: types.Message):
    """Функция срабатывает при нажатии на кнопку Связь с оператором📲"""

    await message.answer("Все вопросы пишите в лс менеджер @bet_market или WhatsApp +7906107766")



@dp.message_handler(commands = ['admin'])
async def admin_menu(message: types.Message):
    """Функция срабатывает по команде /admin"""

    if message.from_user.id in admins:
        await message.answer("Вход в админ панель разрешен!\nЧто вы хотите сделать?", reply_markup=general_admin_keyb)


def get_all_users_and_logs_in_start():
    """Форматируем инфу о пользователях в словарь"""

    users = SQLRequests(conn, cursor).get_users()

    for info in users:
        all_users[info[0]] =     {"ID":info[0], 
                                  "Name":info[1], 
                                  "Username":info[2], 
                                  "Status":info[3],
                                  "Date":info[4]}

    logs_from_db = SQLRequests(conn.cursor).load_actions_from_database()
    if logs_from_db:
        for log in logs_from_db:
            logs[log[0]] = {"Date":log[0],
                            "Action":log[1],
                            "Info":log[2]
            }
    else:
        logs = False


if __name__ == "__main__":
    get_all_users_and_logs_in_start()

    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
    	print(e)
