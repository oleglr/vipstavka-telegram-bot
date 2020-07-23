import schedule
import config
from db_requests import conn, cursor, SQLRequests
from datetime import date

connect_to_db = SQLRequests(conn, cursor)

class WorkWithUsers:

    def __init__(self, conn, cursor, users):

        self.conn = conn
        self.cursor = cursor
        self.users = users

    
    def kick_users(self):
        users = self.users.select_for_kick()



a = WorkWithUsers(conn, cursor, connect_to_db)

a.kick_users()


