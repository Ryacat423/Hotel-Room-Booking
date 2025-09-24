from services.admin_service import AdminService
import pandas as pd

class AdminUI:
    def __init__(self):
        self.admin_service = AdminService()
    
    def authenticate(self):
        print("\n=== ADMIN LOGIN ===")
        try:
            username = input("Enter username: ")
            password = input("Enter password: ")
            
            if self.admin_service.authenticate(username, password):
                print("✓ Login successful!")
                return True
            elif len(username) < 3:
                print("Username too short.")
                return False
            elif len(password) < 6:
                print("Password too short")
                return False
            else:
                print("✗ Invalid credentials!")
                return False
        except Exception as e:
            print(f"✗ Login error: {e}")
            return False
    
    def show_menu(self):
        print("\n=== ADMIN MENU ===")
        print("[1] Amenity Management")
        print("[2] Room Details Management")
        print("[3] Room Management")
        print("[4] Booking Management")
        print("[0] Logout")
        
        try:
            return int(input("Select option: "))
        except ValueError:
            return None
    
    def amenity_menu(self):
        while True:
            print("\n=== AMENITY MANAGEMENT ===")
            print("[1] View All Amenities")
            print("[2] Add Amenity")
            print("[3] Update Amenity")
            print("[4] Delete Amenity")
            print("[0] Back to Main Menu")
            
            try:
                choice = int(input("Select option: "))
            except ValueError:
                choice = None

            match choice:
                case 1:
                    self.view_amenities()
                case 2:
                    self.add_amenity()
                case 3:
                    self.update_amenity()
                case 4:
                    self.delete_amenity()
                case 0:
                    break
                case None:
                    print("\n✗ Invalid input. Please enter a valid number.")
                case _:
                    print("\n✗ Invalid option selected.")
    
    def view_amenities(self):
        try:
            amenities = self.admin_service.get_all_amenities()
            if amenities:
                df = pd.DataFrame(amenities, columns=['Amenity ID', 'Amenity'])
                print("\n" + "="*40)
                print("           AMENITIES")
                print("="*40)
                print(df.to_string(index=False))
            else:
                print("\n✗ No amenities found.")
        except Exception as e:
            print(f"\n✗ Error viewing amenities: {e}")
    
    def add_amenity(self):
        try:
            amenity_name = input("Enter amenity name: ").strip()
            if not amenity_name:
                print("✗ Amenity name cannot be empty.")
                return
                
            if self.admin_service.add_amenity(amenity_name):
                print("✓ Amenity added successfully!")
            else:
                print("✗ Failed to add amenity.")
        except Exception as e:
            print(f"✗ Error adding amenity: {e}")
    
    def update_amenity(self):
        try:
            self.view_amenities()
            amenity_id = int(input("Enter amenity ID to update: "))
            new_name = input("Enter new amenity name: ").strip()
            
            if not new_name:
                print("✗ Amenity name cannot be empty.")
                return
                
            if self.admin_service.update_amenity(amenity_id, new_name):
                print("✓ Amenity updated successfully!")
            else:
                print("✗ Failed to update amenity.")
        except ValueError:
            print("✗ Invalid amenity ID format.")
        except Exception as e:
            print(f"✗ Error updating amenity: {e}")
    
    def delete_amenity(self):
        try:
            self.view_amenities()
            amenity_id = int(input("Enter amenity ID to delete: "))
            confirm = input(f"Are you sure you want to delete amenity ID {amenity_id}? (y/n): ")
            
            if confirm.lower() == 'y':
                if self.admin_service.delete_amenity(amenity_id):
                    print("✓ Amenity deleted successfully!")
                else:
                    print("✗ Failed to delete amenity.")
        except ValueError:
            print("✗ Invalid amenity ID format.")
        except Exception as e:
            print(f"✗ Error deleting amenity: {e}")
    
    def room_details_menu(self):
        while True:
            print("\n=== ROOM DETAILS MANAGEMENT ===")
            print("[1] View All Room Details")
            print("[2] Add Room Detail")
            print("[3] Update Room Detail")
            print("[4] Delete Room Detail")
            print("[0] Back to Main Menu")
            
            try:
                choice = int(input("Select option: "))
            except ValueError:
                choice = None

            match choice:
                case 1:
                    self.view_room_details()
                case 2:
                    self.add_room_detail()
                case 3:
                    self.update_room_detail()
                case 4:
                    self.delete_room_detail()
                case 0:
                    break
                case None:
                    print("\n✗ Invalid input. Please enter a valid number.")
                case _:
                    print("\n✗ Invalid option selected.")
    
    def view_room_details(self):
        try:
            details = self.admin_service.get_all_room_details()
            if details:
                df = pd.DataFrame(details, columns=['Room Type', 'Price'])
                df['Price'] = df['Price'].apply(lambda x: f"{x:.2f}")
                print("\n" + "="*40)
                print("         ROOM DETAILS")
                print("="*40)
                print(df.to_string(index=False))
            else:
                print("\n✗ No room details found.")
        except Exception as e:
            print(f"\n✗ Error viewing room details: {e}")
    
    def add_room_detail(self):
        try:
            room_type = input("Enter room type: ").strip()
            if not room_type:
                print("✗ Room type cannot be empty.")
                return
                
            price = float(input("Enter price: "))
            if price < 0:
                print("✗ Price cannot be negative.")
                return
                
            if self.admin_service.add_room_detail(room_type, price):
                print("✓ Room detail added successfully!")
            else:
                print("✗ Failed to add room detail.")
        except ValueError:
            print("✗ Invalid price format.")
        except Exception as e:
            print(f"✗ Error adding room detail: {e}")
    
    def update_room_detail(self):
        try:
            self.view_room_details()
            room_type = input("Enter room type to update: ").strip()
            if not room_type:
                print("✗ Room type cannot be empty.")
                return
                
            new_price = float(input("Enter new price: "))
            if new_price < 0:
                print("✗ Price cannot be negative.")
                return
                
            if self.admin_service.update_room_detail(room_type, new_price):
                print("✓ Room detail updated successfully!")
            else:
                print("✗ Failed to update room detail.")
        except ValueError:
            print("✗ Invalid price format.")
        except Exception as e:
            print(f"✗ Error updating room detail: {e}")
    
    def delete_room_detail(self):
        try:
            self.view_room_details()
            room_type = input("Enter room type to delete: ").strip()
            if not room_type:
                print("✗ Room type cannot be empty.")
                return
                
            confirm = input(f"Are you sure you want to delete '{room_type}'? (y/n): ")
            if confirm.lower() == 'y':
                if self.admin_service.delete_room_detail(room_type):
                    print("✓ Room detail deleted successfully!")
                else:
                    print("✗ Failed to delete room detail.")
        except Exception as e:
            print(f"✗ Error deleting room detail: {e}")
    
    def room_management_menu(self):
        while True:
            print("\n=== ROOM MANAGEMENT ===")
            print("[1] View All Rooms")
            print("[2] Add Room")
            print("[3] Update Room")
            print("[4] Delete Room")
            print("[0] Back to Main Menu")
            
            try:
                choice = int(input("Select option: "))
            except ValueError:
                choice = None

            match choice:
                case 1:
                    self.view_rooms()
                case 2:
                    self.add_room()
                case 3:
                    self.update_room()
                case 4:
                    self.delete_room()
                case 0:
                    break
                case None:
                    print("\n✗ Invalid input. Please enter a valid number.")
                case _:
                    print("\n✗ Invalid option selected.")
    
    def view_rooms(self):
        try:
            rooms = self.admin_service.get_all_rooms()
            if rooms:
                df = pd.DataFrame(rooms, columns=['Room #', 'Type', 'Capacity', 'Price', 'Amenities'])
                df['Price'] = df['Price'].apply(lambda x: f"{x:.2f}" if x else "N/A")
                df['Amenities'] = df['Amenities'].fillna('None')
                print("\n" + "="*80)
                print("                                ROOMS")
                print("="*80)
                print(df.to_string(index=False))
            else:
                print("\n✗ No rooms found.")
        except Exception as e:
            print(f"\n✗ Error viewing rooms: {e}")
    
    def add_room(self):
        try:
            self.view_room_details()
            
            room_type = input("Enter room type: ").strip()
            if not room_type:
                print("✗ Room type cannot be empty.")
                return
                
            capacity = int(input("Enter room capacity: "))
            if capacity <= 0:
                print("✗ Capacity must be positive.")
                return
            
            self.view_amenities()
            
            amenities_input = input("Enter amenity IDs (comma-separated, or press Enter to skip): ").strip()
            amenity_ids = []
            if amenities_input:
                try:
                    amenity_ids = [int(x.strip()) for x in amenities_input.split(',')]
                except ValueError:
                    print("✗ Invalid amenity ID format.")
                    return
            
            if self.admin_service.add_room(room_type, capacity, amenity_ids):
                print("✓ Room added successfully!")
            else:
                print("✗ Failed to add room.")
        except ValueError:
            print("✗ Invalid input format.")
        except Exception as e:
            print(f"✗ Error adding room: {e}")
    
    def update_room(self):
        try:
            self.view_rooms()
            room_number = int(input("Enter room number to update: "))
            
            current_amenities = self.admin_service.get_room_amenities(room_number)
            if current_amenities:
                print(f"\nCurrent amenities for Room {room_number}:")
                for amenity in current_amenities:
                    print(f"- {amenity[1]}")
            
            room_type = input("Enter new room type: ").strip()
            if not room_type:
                print("✗ Room type cannot be empty.")
                return
                
            capacity = int(input("Enter new capacity: "))
            if capacity <= 0:
                print("✗ Capacity must be positive.")
                return
            
            self.view_amenities()
            
            amenities_input = input("Enter amenity IDs (comma-separated, or press Enter to clear): ").strip()
            amenity_ids = []
            if amenities_input:
                try:
                    amenity_ids = [int(x.strip()) for x in amenities_input.split(',')]
                except ValueError:
                    print("✗ Invalid amenity ID format.")
                    return
            
            if self.admin_service.update_room(room_number, room_type, capacity, amenity_ids):
                print("✓ Room updated successfully!")
            else:
                print("✗ Failed to update room.")
        except ValueError:
            print("✗ Invalid input format.")
        except Exception as e:
            print(f"✗ Error updating room: {e}")
    
    def delete_room(self):
        try:
            self.view_rooms()
            room_number = int(input("Enter room number to delete: "))
            confirm = input(f"Are you sure you want to delete Room {room_number}? (y/n): ")
            
            if confirm.lower() == 'y':
                if self.admin_service.delete_room(room_number):
                    print("✓ Room deleted successfully!")
                else:
                    print("✗ Failed to delete room.")
        except ValueError:
            print("✗ Invalid room number format.")
        except Exception as e:
            print(f"✗ Error deleting room: {e}")
    
    def booking_management_menu(self):
        while True:
            print("\n=== BOOKING MANAGEMENT ===")
            print("[1] View All Bookings")
            print("[2] Cancel Booking")
            print("[0] Back to Main Menu")
            
            try:
                choice = int(input("Select option: "))
            except ValueError:
                choice = None

            match choice:
                case 1:
                    self.view_all_bookings()
                case 2:
                    self.cancel_booking()
                case 0:
                    break
                case None:
                    print("\n✗ Invalid input. Please enter a valid number.")
                case _:
                    print("\n✗ Invalid option selected.")
    
    def view_all_bookings(self):
        try:
            bookings = self.admin_service.get_all_bookings()
            if bookings:
                df = pd.DataFrame(bookings, columns=[
                    'Booking ID', 'First Name', 'Last Name', 'Room #', 
                    'Room Type', 'Check-in', 'Check-out', 'Status', 'Price'
                ])
                df['Price'] = df['Price'].apply(lambda x: f"{x:.2f}" if x else "N/A")
                df['Check-in'] = pd.to_datetime(df['Check-in']).dt.strftime('%Y-%m-%d')
                df['Check-out'] = pd.to_datetime(df['Check-out']).dt.strftime('%Y-%m-%d')
                print("\n" + "="*100)
                print("                                    ALL BOOKINGS")
                print("="*100)
                print(df.to_string(index=False))
            else:
                print("\n✗ No bookings found.")
        except Exception as e:
            print(f"\n✗ Error viewing bookings: {e}")
    
    def cancel_booking(self):
        try:
            self.view_all_bookings()
            booking_id = int(input("Enter booking ID to cancel: "))
            confirm = input(f"Are you sure you want to cancel booking ID {booking_id}? (y/n): ")
            
            if confirm.lower() == 'y':
                if self.admin_service.cancel_booking(booking_id):
                    print("✓ Booking cancelled successfully!")
                else:
                    print("✗ Failed to cancel booking.")
        except ValueError:
            print("✗ Invalid booking ID format.")
        except Exception as e:
            print(f"✗ Error cancelling booking: {e}")
