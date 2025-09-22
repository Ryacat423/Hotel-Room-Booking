from models.base_model import BaseModel
from datetime import datetime

class Booking(BaseModel):
    def get_table_name(self):
        return 'booking'
    
    def create_booking(self, room_number, guest_id, checkin_date, checkout_date):
        booking_date = datetime.now()
        return self.insert(
            ['room_number', 'guest_id', 'booking_date', 'checkin_date', 'checkout_date', 'status'],
            (room_number, guest_id, booking_date, checkin_date, checkout_date, 'confirmed')
        )
    
    def get_bookings_by_guest(self, guest_id):
        return self.select_where(['guest_id'], (guest_id,))
    
    def get_booking_details(self, booking_id):
        query = """
        SELECT b.*, g.firstname, g.lastname, r.room_type, rd.room_price
        FROM booking b
        LEFT JOIN guest g ON b.guest_id = g.guest_id
        LEFT JOIN room r ON b.room_number = r.room_number
        LEFT JOIN room_details rd ON r.room_type = rd.room_type
        WHERE b.booking_id = %s
        """
        return self.db.execute_query(query, fetch=True, params=(booking_id,))
    
    def cancel_booking(self, booking_id):
        return self.update(['status'], ['cancelled'], 'booking_id', booking_id)
    
    def get_all_bookings_detailed(self):
        query = """
        SELECT b.booking_id, g.firstname, g.lastname, b.room_number, r.room_type, 
               b.checkin_date, b.checkout_date, b.status, rd.room_price
        FROM booking b
        LEFT JOIN guest g ON b.guest_id = g.guest_id
        LEFT JOIN room r ON b.room_number = r.room_number
        LEFT JOIN room_details rd ON r.room_type = rd.room_type
        ORDER BY b.booking_id DESC
        """
        return self.db.execute_query(query, fetch=True)
