import sqlite3


class Database:

    def __init__(self, folder, db_name, db_table):
        self.folder = folder
        self.db_name = db_name
        self.db_table = db_table
        self.db_connection = None
        self.db_cursor = None


    def setup(self):
        self.db_connection = sqlite3.connect('%s/%s' % (self.folder, self.db_name))
        self.db_cursor = self.db_connection.cursor()


    def close(self):
        if self.db_connection:
            self.db_cursor = None
            self.db_connection.close()
            self.db_connection = None


    def flush(self):
        query = 'DELETE FROM {};'.format(self.db_table)
        self.db_cursor.execute(query);
        self.db_connection.commit()


    def __del__(self):
        if self.db_connection:
            self.db_connection.close()

