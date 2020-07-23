import sqlite3
from datetime import date
import datetime

today = datetime.datetime.today()

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
    
    def change_status(self, date, chat_id, status):

        request = f"UPDATE users SET Status = ?, Date = ? WHERE ID = ?"
        
        self.cursor.execute(request, (status, date, chat_id))
        self.conn.commit()


    def select_for_kick(self):
        """Собираем пользователей для удаления"""
        
        now = str(date.today())


        self.cursor.execute(f"SELECT * FROM users WHERE Date = (?) AND Status = ?", [now, "In_Channel"])
        
        res = self.cursor.fetchall()

        return res
    
    def select_for_notate(self, date_1, date_2):
        """Собираем пользователей для оповещения"""

        self.cursor.execute(f"SELECT * FROM users WHERE Date = (?) OR DATE = (?) AND Status = ?", [date_1,date_2, "In_Channel"])

        res = self.cursor.fetchall()

        return res









