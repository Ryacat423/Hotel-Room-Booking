from db.db import execute_query

def show_tables():
    return execute_query("SHOW TABLES", fetch=True)

def select_all(table_name):
    query = f"SELECT * FROM {table_name}"
    return execute_query(query, fetch=True)

def select_where(table_name, columns, values):
    where_expr = ' AND '.join([f"{col} = %s" for col in columns])
    query = f"SELECT * FROM {table_name} WHERE {where_expr}"
    return execute_query(query, fetch=True, params=values)

def insert(table_name, columns, values):
    cols = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(values))
    query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
    execute_query(query, params=values)

def update(table_name, set_columns, set_values, condition_column, condition_value):
    set_expr = ', '.join([f"{col} = %s" for col in set_columns])
    query = f"UPDATE {table_name} SET {set_expr} WHERE {condition_column} = %s"
    execute_query(query, params=tuple(set_values) + (condition_value,))

def delete(table_name, condition_column, condition_value):
    query = f"DELETE FROM {table_name} WHERE {condition_column} = %s"
    execute_query(query, params=(condition_value,))
