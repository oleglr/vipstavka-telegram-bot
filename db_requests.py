import sqlite3


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

get_from_db = SQLRequests(conn, cursor)

print(get_from_db.get_users())