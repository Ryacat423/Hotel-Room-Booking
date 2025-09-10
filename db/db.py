from connection import connect_to_mysql

config = {
  'user': 'root',
  'password': '',
  'host': 'localhost',
  'raise_on_warnings': True
}

connect = connect_to_mysql(config, attempts=3)

if connect and connect.is_connected():
    with connect.cursor() as cursor:
        cursor.execute("USE hotel_booking")

else:
    print("Could not connect")
    connect = None

def execute_query(query, fetch=False, params=None):
    """
    Executes a SQL query.
    
    :param query: SQL query string
    :param fetch: True if you want to fetch results (SELECT)
    :param params: Optional tuple of parameters for parameterized queries
    :return: fetched results if fetch=True, otherwise None
    """
    if not connect or not connect.is_connected():
        print("No database connection")
        return None
    
    with connect.cursor() as cursor:
        cursor.execute(query, params)
        
        if fetch:
            return cursor.fetchall()

        if query.strip().split()[0].upper() in ["INSERT", "UPDATE", "DELETE"]:
            connect.commit()