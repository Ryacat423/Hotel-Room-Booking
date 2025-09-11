from connection import connect_to_mysql
from utils.crud import *
import hashlib

loggedIn = False

config = {
  'user': 'root',
  'password': '',
  'host': 'localhost',
  'database': 'hotel_booking',
  'raise_on_warnings': True
}

connect = connect_to_mysql(config, attempts=3)

def authenticate(username, password):
    hashed_password = hashlib.sha1(password.encode()).hexdigest()
    result = select_where('admin', ['username', 'password'], (username, hashed_password))
    
    return bool(result)

def show_options():
    print("[0] Show all Details")
    print("[1] Add Room Details")
    print("[2] Update Room Details")
    print("[3] Delete Room Details")

username = input("Enter username: ")
password = input("Enter password: ")

if authenticate(username, password):
    print("logged in")
    while True:
        show_options()
        option = int(input("Enter option: "))
        match option:
            case 0:
                tables = select_all("room_details")
                for rows in tables:
                    print(rows)
            case 1:
                room_type = input("Room Type: ")
                price = float(input("Price: "))
                insert("room_details", ["room_type", "room_price"], (room_type, price))
                print("Room added successfully.")

            case 2:
                room_type = input("Room Type to update: ")
                new_price = float(input("New Price: "))
                update("room_details", ["room_price"], [new_price], "room_type", room_type)
                print("Room updated successfully.")

            case 3:
                room_type = input("Room Type to delete: ")
                delete("room_details", "room_type", room_type)
                print("Room deleted successfully.")
else:
    print("may mali gar")