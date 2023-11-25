import sqlite3


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS staff (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                surname TEXT,
                password TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                staff_id INTEGER,
                currency_in TEXT,
                currency_out TEXT,
                amount INTEGER,
                date TEXT,
                time TEXT,
                FOREIGN KEY (staff_id) REFERENCES staff(id)
            )
        ''')

        self.conn.commit()

    def new_user(self, name, surname, password):
        try:
            self.cursor.execute('''
                INSERT INTO staff (name, surname, password) VALUES (?, ?, ?)
            ''', (name, surname, password))
            self.conn.commit()
            user_id = self.cursor.lastrowid
            return user_id  # all successfully
        except Exception as e:
            # add logging
            return -1  # error

    def check_user_password(self, user_id, password):
        self.cursor.execute('SELECT password FROM staff WHERE id = ?', (user_id,))
        password_db = self.cursor.fetchone()
        if password_db is None:
            return -1  # user not found
        elif str(password) == str(password_db[0]):
            return 0  # all successfully
        elif password != password_db:
            return 1  # wrong password
        else:
            return -2  # unknown error

    def close_connection(self):
        self.conn.close()

    def new_log(self, staff_id, currency_in, currency_out, amount, date, time):
        try:
            self.cursor.execute('''
                INSERT INTO operations (staff_id, currency_in, currency_out, amount, time) VALUES (?, ?, ?, ?, ?, ?)
            ''', (staff_id, currency_in, currency_out, amount, date, time))
            self.conn.commit()
            return 0  # all successfully
        except Exception as e:
            # add logging
            return -1  # error


if __name__ == '__main__':
    db = DataBase()
    db.close_connection()
