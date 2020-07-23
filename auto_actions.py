import schedule
import config
from db_requests import conn, cursor, SQLRequests
from datetime import date, timedelta
from config import API_TOKEN, admins, chat_id
import requests
import time



r = requests.Session()
url = "https://api.telegram.org/bot{0}/".format(API_TOKEN)

connect_to_db = SQLRequests(conn, cursor)


class WorkWithUsers:

    def kick_users(self):
        users = connect_to_db.select_for_kick()
        if users:
            try:
                for item in users:

                #Удаляем пользователя
                    r.post(url+"kickChatMember", params = {'chat_id': chat_id, 'user_id': item[0]})

                #Сообщение об удалении пользователю
                    r.post(url+"sendMessage", params = {'chat_id': item[0], 
                                                        'text':"Ваша подписка истекла.\nВы исключены из канала!\n"
                                                        "Можете приобрести ее тем же способом."})
                #Уведомляем админа
                    r.post(url+"sendMessage", params = {'chat_id': admins[0], 
                                                        'text':f'Пользователь {item[0]} удален из канала.\n'
                                                        f'{item[1]}\n'
                                                        f'@{item[2]}'
                                                        }
                                                        )
                    connect_to_db.change_status(str(date.today()), item[0], "NULL")

            except Exception:
                pass
    
    def notate_user_and_admin(self):
        one_day = date.today() - timedelta(1)
        three_days = date.today() - timedelta(3)

        users = connect_to_db.select_for_notate(str(one_day), str(three_days))


        if users:
            try:
                for item in users:
                    print(item[4], one_day)

                    if item[4] == str(three_days):

                        r.post(url+"sendMessage", params = {'chat_id': item[0], 
                                                            'text': "У вас осталось 3 дня до окончания подписки.\n"
                                                            "Продлите ее таким же способом как и приобрели.\n Связь с менеджером @bet_market или ватсап +7906107766"})
                    if item[4] == str(one_day):
                        r.post(url+"sendMessage", params = {'chat_id': item[0], 
                                                            'text': "У вас остался 1 день до окончания подписки.\n"
                                                            "Продлите ее таким же способом как и приобрели.\nСвязь с менеджером @bet_market или ватсап +7906107766"})

                        r.post(url+"sendMessage", params = {'chat_id': admins[0], 
                                                        'text':f'Пользователь {item[0]} 1 день до окончания подписки.\n'
                                                        f'{item[1]}\n'
                                                        f'@{item[2]}'
                                                        }
                                                        )
            except Exception:
                pass



def job():

    kick = WorkWithUsers().kick_users()
    a = WorkWithUsers().notate_user_and_admin()



schedule.every().day.at("00:00").do(job)


while True:
    schedule.run_pending()
    time.sleep(1)
