import pyodbc

class SQLServer():

    def __init__(self):
        server = '10.xx.xx.xx' 
        database = 'csv_test' 
        username = 'xxx' 
        password = 'xxx' 
        string_connection = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        self.connection = pyodbc.connect(string_connection)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.connection.close()

    def open_cursor(self):
        return self.cursor
    
    def close_cursor(self):
        self.cursor.close()
        self.connection.close()
