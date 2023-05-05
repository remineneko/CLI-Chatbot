import mysql.connector

class DBSession:
    def __init__(self, host, user_name, password):
        self.access = mysql.connector.connect(
            host = host,
            user = user_name,
            password = password,
            use_unicode = True,
            charset = 'utf8'
        )

        self.dbcursor = self.access.cursor(buffered = True)
        self._db_name = "Chatbot"
        self._create_database()
        self._create_table()

    def _create_database(self):
        self.dbcursor.execute(f"CREATE DATABASE IF NOT EXISTS {self._db_name};")
        self.access.commit()

    def _use_db(self, cmd, args = None):
        self.dbcursor.execute(f"USE {self._db_name};")
        self.access.commit()

        if args:
            self.dbcursor.execute(cmd, args)
        else:
            self.dbcursor.execute(cmd)
        self.access.commit()

    def _create_table(self):
        cmd = "CREATE TABLE IF NOT EXISTS ChatSession (chat_id INT NOT NULL AUTO_INCREMENT, created_date DATETIME, updated_date DATETIME, history_file_name VARCHAR(255), PRIMARY KEY (chat_id));"
        self._use_db(cmd)

    def save_session(self, file_name):
        cmd = f"INSERT IGNORE INTO ChatSession (created_date, updated_date, history_file_name) VALUES (NOW(), NOW(), %(history_file_name)s);"
        args = {
            "history_file_name": file_name
        }
        self._use_db(cmd, args)

    def update_history(self, file_name):
        cmd = "UPDATE ChatSession SET updated_date = NOW() WHERE history_file_name=%(history_file_name)s;"
        args = {
            "history_file_name": file_name
        }
        self._use_db(cmd, args)

    def get_history(self):
        cmd = "SELECT * FROM ChatSession;"
        self._use_db(cmd)
        entries = self.dbcursor.fetchall()
        return entries