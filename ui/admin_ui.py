from services.admin_service import AdminService

class AdminUI:
    def __init__(self):
        self.admin_service = AdminService()
    
    def authenticate(self):
        print("\n=== ADMIN LOGIN ===")
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        if self.admin_service.authenticate(username, password):
            print("✓ Login successful!")
            return True
        else:
            print("✗ Invalid credentials!")
            return False
    
    def show_menu(self):
        print("\n=== ADMIN MENU ===")
        print("[1] Room Details Management")
        print("[2] Room Management")
        print("[3] Booking Management")
        print("[4] View All Bookings")
        print("[5] Print Reports")
        print("[6] Test Printer")
        print("[0] Logout")
        return input("Select option: ")
    
    def room_details_menu(self):
        while True:
            print("\n=== ROOM DETAILS MANAGEMENT ===")
            print("[1] View All Room Details")
            print("[2] Add Room Detail")
            print("[3] Update Room Detail")
            print("[4] Delete Room Detail")
            print("[5] Print Room Details Report")
            print("[0] Back to Main Menu")
            
            choice = input("Select option: ")
            
            if choice == "1":
                self.view_room_details()
            elif choice == "2":
                self.add_room_detail()
            elif choice == "3":
                self.update_room_detail()
            elif choice == "4":
                self.delete_room_detail()
            elif choice == "5":
                self.print_rooms_report()
            elif choice == "0":
                break
    
    def view_room_details(self):
        details = self.admin_service.get_all_room_details()
        if details:
            print("\nRoom Details:")
            print(f"{'Room Type':<20} {'Price':<10}")
            print("-" * 30)
            for detail in details:
                print(f"{detail[0]:<20} ${detail[1]:<10.2f}")
        else:
            print("No room details found.")
    
    def add_room_detail(self):
        room_type = input("Enter room type: ")
        try:
            price = float(input("Enter price: "))
            if self.admin_service.add_room_detail(room_type, price):
                print("✓ Room detail added successfully!")
            else:
                print("✗ Failed to add room detail.")
        except ValueError:
            print("✗ Invalid price format.")
    
    def update_room_detail(self):
        room_type = input("Enter room type to update: ")
        try:
            new_price = float(input("Enter new price: "))
            if self.admin_service.update_room_detail(room_type, new_price):
                print("✓ Room detail updated successfully!")
            else:
                print("✗ Failed to update room detail.")
        except ValueError:
            print("✗ Invalid price format.")
    
    def delete_room_detail(self):
        room_type = input("Enter room type to delete: ")
        confirm = input(f"Are you sure you want to delete '{room_type}'? (y/n): ")
        if confirm.lower() == 'y':
            if self.admin_service.delete_room_detail(room_type):
                print("✓ Room detail deleted successfully!")
            else:
                print("✗ Failed to delete room detail.")
    
    def print_reports_menu(self):
        print("\n=== PRINT REPORTS ===")
        print("[1] Print Rooms Report")
        print("[2] Print Bookings Report")
        print("[3] Test Printer")
        print("[0] Back to Main Menu")
        
        choice = input("Select option: ")
        
        if choice == "1":
            self.print_rooms_report()
        elif choice == "2":
            self.print_bookings_report()
        elif choice == "3":
            self.test_printer()
    
    def print_rooms_report(self):
        print("Printing rooms report...")
        if self.admin_service.print_rooms_report():
            print("✓ Rooms report printed successfully!")
        else:
            print("✗ Failed to print rooms report.")
    
    def print_bookings_report(self):
        print("Printing bookings report...")
        if self.admin_service.print_bookings_report():
            print("✓ Bookings report printed successfully!")
        else:
            print("✗ Failed to print bookings report.")
    
    def test_printer(self):
        print("Testing printer connection...")
        if self.admin_service.test_printer():
            print("✓ Printer test successful!")
        else:
            print("✗ Printer test failed. Check connection and configuration.")

