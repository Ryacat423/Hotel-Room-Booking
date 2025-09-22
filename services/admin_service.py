from models.admin import Admin
from models.room_details import RoomDetails
from models.room import Room
from models.booking import Booking
from models.guest import Guest
from models.amenity import Amenity
from models.room_amenities import RoomAmenities

class AdminService:
    def __init__(self):
        self.admin = Admin()
        self.room_details = RoomDetails()
        self.room = Room()
        self.booking = Booking()
        self.guest = Guest()
        self.amenity = Amenity()
        self.room_amenities = RoomAmenities()
    
    def authenticate(self, username, password):
        return self.admin.authenticate(username, password)
    
    # Amenity Management
    def get_all_amenities(self):
        return self.amenity.get_all_amenities()
    
    def add_amenity(self, amenity_name):
        return self.amenity.create_amenity(amenity_name)
    
    def update_amenity(self, amenity_id, amenity_name):
        return self.amenity.update_amenity(amenity_id, amenity_name)
    
    def delete_amenity(self, amenity_id):
        return self.amenity.delete_amenity(amenity_id)
    
    # Room Details Management
    def get_all_room_details(self):
        return self.room_details.select_all()
    
    def add_room_detail(self, room_type, room_price):
        return self.room_details.insert(['room_type', 'room_price'], (room_type, room_price))
    
    def update_room_detail(self, room_type, new_price):
        return self.room_details.update(['room_price'], [new_price], 'room_type', room_type)
    
    def delete_room_detail(self, room_type):
        return self.room_details.delete('room_type', room_type)
    
    # Room Management
    def get_all_rooms(self):
        return self.room.get_all_rooms_with_details()
    
    def add_room(self, room_type, capacity, amenity_ids):
        if self.room.create_room(room_type, capacity):
            room_number = self.room.get_last_room_number()
            if room_number and amenity_ids:
                for amenity_id in amenity_ids:
                    self.room_amenities.assign_amenity_to_room(room_number, amenity_id)
            return True
        return False
    
    def update_room(self, room_number, room_type, capacity, amenity_ids):
        if self.room.update(['room_type', 'capacity'], [room_type, capacity], 'room_number', room_number):
            self.room_amenities.clear_room_amenities(room_number)
            if amenity_ids:
                for amenity_id in amenity_ids:
                    self.room_amenities.assign_amenity_to_room(room_number, amenity_id)
            return True
        return False
    
    def delete_room(self, room_number):
        self.room_amenities.clear_room_amenities(room_number)
        return self.room.delete('room_number', room_number)
    
    def get_room_amenities(self, room_number):
        return self.room_amenities.get_room_amenities(room_number)
    
    # Booking Management
    def get_all_bookings(self):
        return self.booking.get_all_bookings_detailed()
    
    def get_booking_details(self, booking_id):
        return self.booking.get_booking_details(booking_id)
    
    def cancel_booking(self, booking_id):
        return self.booking.cancel_booking(booking_id)
