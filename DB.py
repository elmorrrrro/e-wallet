import sqlite3


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('finance.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS finance(id integer primary key, description text, costs text, total real, 
            dates text)''')
        self.conn.commit()

    def insert_data(self, description, costs, total, dates):
        self.c.execute('''INSERT INTO finance(description, costs, total, dates) VALUES (?, ?, ?, ?)''',
                       (description, costs, total, dates))
        # saving
        self.conn.commit()
