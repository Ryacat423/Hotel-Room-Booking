from services.booking_service import BookingService
from datetime import datetime
import pandas as pd

class UserUI:
    def __init__(self):
        self.booking_service = BookingService()
    
    def show_menu(self):
        print("\n=== HOTEL BOOKING SYSTEM ===")
        print("[1] View Available Rooms")
        print("[2] Make a Booking")
        print("[3] View My Bookings")
        print("[0] Exit")
        
        try:
            return int(input("Select option: "))
        except ValueError:
            return None
    
    def view_available_rooms(self):
        try:
            # checkin = input("Enter check-in date (YYYY-MM-DD): ").strip()
            # checkout = input("Enter check-out date (YYYY-MM-DD): ").strip()
            
            # checkin_date = datetime.strptime(checkin, "%Y-%m-%d")
            # checkout_date = datetime.strptime(checkout, "%Y-%m-%d")
            
            # if checkin_date >= checkout_date:
            #     print("✗ Check-out date must be after check-in date.")
            #     return
            
            rooms = self.booking_service.get_all_rooms()
            
            if rooms:
                df = pd.DataFrame(rooms, columns=['Room #', 'Type', 'Capacity', 'Price', 'Amenities'])
                df['Price'] = df['Price'].apply(lambda x: f"{x:.2f}" if x else "N/A")
                
                print(f"\n" + "="*70)
                # print(f"         ROOMS AVAILABILITY ({checkin} to {checkout})")
                print("="*70)
                print(df.to_string(index=False))
                
                # available_df = df[df['Status'] == 'Available']
                # if not available_df.empty:
                #     print(f"\n" + "="*70)
                #     print("                    AVAILABLE ROOMS")
                #     print("="*70)
                #     print(available_df.to_string(index=False))
                # else:
                #     print("\n✗ No rooms available for the selected dates.")
                
        except ValueError:
            print("✗ Invalid date format. Please use YYYY-MM-DD.")
        except Exception as e:
            print(f"✗ Error viewing rooms: {e}")
    
    def make_booking(self):
        print("\n=== MAKE BOOKING ===")
        
        try:
            contact = input("Enter your contact number: ").strip()
            if not contact:
                print("✗ Contact number cannot be empty.")
                return
            
            existing_guest = self.booking_service.find_guest_by_contact(contact)
            
            if existing_guest:
                guest_id = existing_guest[0][0]
                print(f"✓ Welcome back, {existing_guest[0][1]} {existing_guest[0][2]}!")
            else:
                print("\n--- New Guest Registration ---")
                firstname = input("First name: ").strip()
                lastname = input("Last name: ").strip()
                middlename = input("Middle name (optional): ").strip()
                
                while True:
                    gender = input("Gender (M/F): ").strip().upper()
                    if gender in ['M', 'F']:
                        break
                    print("✗ Please enter 'M' for Male or 'F' for Female.")
                
                if not firstname or not lastname:
                    print("✗ First name and last name are required.")
                    return
                
                guest_id = self.booking_service.create_guest(firstname, lastname, middlename, gender, contact)
                if not guest_id:
                    print("✗ Failed to register guest.")
                    return
                print("✓ Guest registered successfully!")
            
            checkin = input("Enter check-in date (YYYY-MM-DD): ").strip()
            checkout = input("Enter check-out date (YYYY-MM-DD): ").strip()
            
            checkin_date = datetime.strptime(checkin, "%Y-%m-%d").date()
            checkout_date = datetime.strptime(checkout, "%Y-%m-%d").date()
            
            if checkin_date >= checkout_date:
                print("✗ Check-out date must be after check-in date.")
                return
            
            if checkin_date < datetime.now().date():
                print("✗ Check-in date cannot be in the past.")
                return
            
            rooms = self.booking_service.get_available_rooms_with_status(checkin_date, checkout_date)
            available_rooms = [room for room in rooms if room[4] == 'Available']
            
            if not available_rooms:
                print("✗ No rooms available for the selected dates.")
                return
            
            df = pd.DataFrame(available_rooms, columns=['Room #', 'Type', 'Capacity', 'Price', 'Status'])
            df['Price'] = df['Price'].apply(lambda x: f"{x:.2f}" if x else "N/A")
            
            print(f"\n" + "="*70)
            print("                    AVAILABLE ROOMS")
            print("="*70)
            print(df.to_string(index=False))
            
            print(f"\n" + "="*70)
            print("                   ROOM DETAILS")
            print("="*70)
            
            for room in available_rooms:
                room_details = self.booking_service.get_room_details(room[0])
                if room_details:
                    detail = room_details[0]
                    amenities = detail[4] if detail[4] else "None"
                    print(f"Room {detail[0]} - {detail[1]} | Capacity: {detail[2]} | Price: {detail[3]:.2f}")
                    print(f"Amenities: {amenities}")
                    print("-" * 70)
            
            room_number = int(input("\nEnter room number to book: "))
            
            if not any(room[0] == room_number for room in available_rooms):
                print("✗ Invalid room selection or room not available.")
                return
            
            selected_room = next(room for room in available_rooms if room[0] == room_number)
            nights = (checkout_date - checkin_date).days
            total_cost = selected_room[3] * nights if selected_room[3] else 0
            
            print(f"\n--- Booking Summary ---")
            print(f"Room: {room_number} ({selected_room[1]})")
            print(f"Check-in: {checkin}")
            print(f"Check-out: {checkout}")
            print(f"Nights: {nights}")
            print(f"Rate per night: {selected_room[3]:.2f}")
            print(f"Total Cost: {total_cost:.2f}")
            
            confirm = input("\nConfirm booking? (y/n): ")
            if confirm.lower() != 'y':
                print("✗ Booking cancelled.")
                return
            
            booking_id = self.booking_service.create_booking(room_number, guest_id, 
                                                        datetime.combine(checkin_date, datetime.min.time()),
                                                        datetime.combine(checkout_date, datetime.min.time()))
            
            if booking_id:
                print(f"✓ Booking confirmed! Booking ID: {booking_id}")
                print(f"✓ Total Amount: {total_cost:.2f}")
            else:
                print("✗ Failed to create booking.")
                
        except ValueError as e:
            if "time data" in str(e):
                print("✗ Invalid date format. Please use YYYY-MM-DD.")
            else:
                print("✗ Invalid input format.")
        except Exception as e:
            print(f"✗ Error making booking: {e}")


    def view_my_bookings(self):
        try:
            contact = input("Enter your contact number: ").strip()
            if not contact:
                print("✗ Contact number cannot be empty.")
                return
            
            guest = self.booking_service.find_guest_by_contact(contact)
            if not guest:
                print("✗ No guest found with this contact number.")
                return
            
            guest_id = guest[0][0]
            bookings = self.booking_service.get_guest_bookings(guest_id)
            
            if bookings:
                booking_data = []
                for booking in bookings:
                    booking_data.append([
                        booking[0],
                        booking[2],
                        booking[4].strftime('%Y-%m-%d'),
                        booking[5].strftime('%Y-%m-%d'),
                        booking[6]
                    ])
                
                df = pd.DataFrame(booking_data, columns=[
                    'Booking ID', 'Room #', 'Check-in', 'Check-out', 'Status'
                ])
                
                print(f"\n" + "="*60)
                print("                YOUR BOOKINGS")
                print("="*60)
                print(df.to_string(index=False))
            else:
                print("✗ No bookings found for this contact.")
                
        except Exception as e:
            print(f"✗ Error viewing bookings: {e}")
