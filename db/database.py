from connection import DatabaseConnection
import mysql.connector

class Database:
    def __init__(self):
        self.db_connection = DatabaseConnection()
        self.connection = self.db_connection.get_connection()
    
    def execute_query(self, query, fetch=False, params=None):
        if not self.connection or not self.connection.is_connected():
            print("No database connection")
            return None
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                
                if fetch:
                    return cursor.fetchall()
                
                if query.strip().split()[0].upper() in ["INSERT", "UPDATE", "DELETE"]:
                    self.connection.commit()
                    return cursor.rowcount
                    
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            self.connection.rollback()
            return None
    
    def close(self):
        self.db_connection.close()