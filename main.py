from ui.admin_ui import AdminUI
from ui.user_ui import UserUI

def main():
    admin_ui = AdminUI()
    user_ui = UserUI()
    
    while True:
        print("\n" + "="*50)
        print("    HOTEL ROOM BOOKING SYSTEM")
        print("="*50)
        print("[1] Admin Login")
        print("[2] Customer Booking")
        print("[0] Exit")
        
        choice = input("Select option: ")
        
        if choice == "1":
            if admin_ui.authenticate():
                admin_menu(admin_ui)
        elif choice == "2":
            customer_menu(user_ui)
        elif choice == "0":
            print("Thank you for using Hotel Booking System!")
            break
        else:
            print("Invalid option. Please try again.")

def admin_menu(admin_ui):
    while True:
        choice = admin_ui.show_menu()
        
        if choice == "1":
            admin_ui.room_details_menu()
        elif choice == "2":
            print("Room management coming soon...")
        elif choice == "3":
            print("Booking management coming soon...")
        elif choice == "4":
            print("View all bookings coming soon...")
        elif choice == "6":
            admin_ui.test_printer()
        elif choice == "0":
            print("Logged out successfully!")
            break
        else:
            print("Invalid option. Please try again.")

def customer_menu(user_ui):
    while True:
        choice = user_ui.show_menu()
        
        if choice == "1":
            user_ui.view_available_rooms()
        elif choice == "2":
            user_ui.make_reservation()
        elif choice == "3":
            print("View bookings coming soon...")
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
