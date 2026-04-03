import sqlite3

class DBManager:

    def __init__(self,db_file_uri):
        self.conn = sqlite3.connect(db_file_uri)
        self.cursor = self.conn.cursor()
    
    def execute(self, query,values=None):
        if values is None:
            return self.cursor.execute(query)
        else:
            return self.cursor.execute(query,tuple(values))

    def commit(self):
        self.conn.commit()
        
        
