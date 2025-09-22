from ui.admin_ui import AdminUI
from ui.user_ui import UserUI

def main():
    admin_ui = AdminUI()
    user_ui = UserUI()
    
    while True:
        print("\n" + "="*50)
        print("HOTEL ROOM BOOKING SYSTEM")
        print("="*50)
        print("[1] Admin Login")
        print("[2] Customer Booking")
        print("[0] Exit")
        
        try:
            choice = int(input("Select option: "))
        except ValueError:
            choice = None
        
        match choice:
            case 1:
                if admin_ui.authenticate():
                    admin_menu(admin_ui)
            case 2:
                customer_menu(user_ui)
            case 0:
                print("Thank you for using Hotel Booking System!")
                break
            case None:
                print("✗ Invalid input. Please enter a valid number.")
            case _:
                print("✗ Invalid option. Please try again.")

def admin_menu(admin_ui):
    while True:
        try:
            choice = admin_ui.show_menu()
        except KeyboardInterrupt:
            print("\n\nLogged out successfully!")
            break
        
        match choice:
            case 1:
                admin_ui.amenity_menu()
            case 2:
                admin_ui.room_details_menu()
            case 3:
                admin_ui.room_management_menu()
            case 4:
                admin_ui.booking_management_menu()
            case 0:
                print("✓ Logged out successfully!")
                break
            case None:
                print("✗ Invalid input. Please enter a valid number.")
            case _:
                print("✗ Invalid option. Please try again.")

def customer_menu(user_ui):
    while True:
        try:
            choice = user_ui.show_menu()
        except KeyboardInterrupt:
            print("\n\nReturning to main menu...")
            break
        
        match choice:
            case 1:
                user_ui.view_available_rooms()
            case 2:
                user_ui.make_booking()
            case 3:
                user_ui.view_my_bookings()
            case 0:
                break
            case None:
                print("✗ Invalid input. Please enter a valid number.")
            case _:
                print("✗ Invalid option. Please try again.")

if __name__ == "__main__":
    main()
