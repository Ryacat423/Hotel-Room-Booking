from models.guest import Guest
from models.room import Room
from models.booking import Booking
from datetime import datetime

class BookingService:
    def __init__(self):
        self.guest = Guest()
        self.room = Room()
        self.booking = Booking()
    
    def get_available_rooms_with_status(self, checkin_date, checkout_date):
        return self.room.get_available_rooms(checkin_date, checkout_date)
    
    def create_guest(self, firstname, lastname, middlename, gender, contact_info):
        return self.guest.create_guest(firstname, lastname, middlename, gender, contact_info)
    
    def find_guest_by_contact(self, contact_info):
        return self.guest.get_guest_by_contact(contact_info)
    
    def create_booking(self, room_number, guest_id, checkin_date, checkout_date):
        return self.booking.create_booking(room_number, guest_id, checkin_date, checkout_date)
    
    def get_room_details(self, room_number):
        return self.room.get_room_with_details(room_number)
    
    def get_guest_bookings(self, guest_id):
        return self.booking.get_bookings_by_guest(guest_id)
    
    def get_all_rooms(self):
        return self.room.get_all_rooms_with_details()
