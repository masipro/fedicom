import sqlite3
from config import Config

class SQLite:
    def __init__(self):
        self.connection = sqlite3.connect(Config.SQLITE_DB_PATH)
        self.cursor = self.connection.cursor()

sqlite = SQLite()
