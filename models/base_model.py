from abc import ABC, abstractmethod
from db.database import Database

class BaseModel(ABC):
    def __init__(self):
        self.db = Database()
    
    @abstractmethod
    def get_table_name(self):
        pass
    
    def select_all(self):
        query = f"SELECT * FROM {self.get_table_name()}"
        return self.db.execute_query(query, fetch=True)
    
    def select_by_id(self, id_column, id_value):
        query = f"SELECT * FROM {self.get_table_name()} WHERE {id_column} = %s"
        return self.db.execute_query(query, fetch=True, params=(id_value,))
    
    def select_where(self, columns, values):
        where_expr = ' AND '.join([f"{col} = %s" for col in columns])
        query = f"SELECT * FROM {self.get_table_name()} WHERE {where_expr}"
        return self.db.execute_query(query, fetch=True, params=values)
    
    def insert(self, columns, values):
        cols = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {self.get_table_name()} ({cols}) VALUES ({placeholders})"
        return self.db.execute_query(query, params=values)
    
    def update(self, set_columns, set_values, condition_column, condition_value):
        set_expr = ', '.join([f"{col} = %s" for col in set_columns])
        query = f"UPDATE {self.get_table_name()} SET {set_expr} WHERE {condition_column} = %s"
        return self.db.execute_query(query, params=tuple(set_values) + (condition_value,))
    
    def delete(self, condition_column, condition_value):
        query = f"DELETE FROM {self.get_table_name()} WHERE {condition_column} = %s"
        return self.db.execute_query(query, params=(condition_value,))
