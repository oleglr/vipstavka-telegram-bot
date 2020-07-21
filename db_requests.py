import sqlite3
import datetime

today = datetime.datetime.today()
now = today.strftime("%Y-%m-%d-%H-%M-%S")

logs = {}
conn = sqlite3.connect( "./data/data.db", check_same_thread=False )
cursor = conn.cursor()

class SQLRequests:
    """Класс для работы с базой данных"""

    def __init__(self, conn, cursor):
        """Инициализируем конект и курсор для работой с БД"""

        self.conn = conn
        self.cursor = cursor

    def get_users(self):
        """Собираем инфу о всех пользователях"""
        request = "SELECT * FROM `users`"

        result = self.cursor.execute(request)
        
        return result.fetchall()

    def write_new_user(self, user_id, name, username, status, date):
        """Записываем нового пользователя"""

        request = "INSERT INTO users VALUES(?,?,?,?,?)"
        self.cursor.execute(request, (user_id, name, username, status, date))
        self.conn.commit()
    
    def add_action(self, date, action, user_id, name, userlink):
        """Добавляем действие в БД"""

        request = "INSERT INTO logs (date, action, info) VALUES(?,?,?)"
        
        self.cursor.execute(request, (f"{date}", f"{action}", f"{user_id}|{name}|@{userlink}"))
        self.conn.commit()
    
    def load_actions_from_database(self):
        """Загружаем историю действи из БД"""

        request = "SELECT * FROM `logs`"

        cursor.execute(request)

        result = cursor.fetchall()

        if result != []:
            return result
        
        else:
            return False



a = SQLRequests(conn, cursor)


result = a.load_actions_from_database()



for log in result:
    logs[log[0]] = {"Date":log[1],
                    "Action":log[2],
                    "Info":log[3]}
    
print(logs)

with open("./logs.txt", 'a', encoding='UTF-8') as write_logs:
    for key, val in logs.items():
        write_logs.write(f"{key}: {val}\n")

