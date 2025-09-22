from models.base_model import BaseModel

class Room(BaseModel):
    def get_table_name(self):
        return 'room'
    
    def get_available_rooms(self, checkin_date, checkout_date):
        query = """
        SELECT r.room_number, r.room_type, r.capacity, rd.room_price,
               CASE 
                   WHEN b.room_number IS NOT NULL THEN 'Occupied'
                   ELSE 'Available'
               END as status
        FROM room r
        LEFT JOIN room_details rd ON r.room_type = rd.room_type
        LEFT JOIN booking b ON r.room_number = b.room_number 
            AND b.status = 'confirmed'
            AND (
                (b.checkin_date <= %s AND b.checkout_date > %s) OR
                (b.checkin_date < %s AND b.checkout_date >= %s) OR
                (b.checkin_date >= %s AND b.checkout_date <= %s)
            )
        """
        return self.db.execute_query(query, fetch=True, 
                                   params=(checkin_date, checkin_date, checkout_date, 
                                         checkout_date, checkin_date, checkout_date))
    
    def get_room_with_details(self, room_number):
        query = """
        SELECT r.room_number, r.room_type, r.capacity, rd.room_price,
               GROUP_CONCAT(a.amenity SEPARATOR ', ') as amenities
        FROM room r 
        LEFT JOIN room_details rd ON r.room_type = rd.room_type 
        LEFT JOIN room_amenities ra ON r.room_number = ra.room_number
        LEFT JOIN amenity a ON ra.amenity_id = a.amenity_id
        WHERE r.room_number = %s
        GROUP BY r.room_number
        """
        return self.db.execute_query(query, fetch=True, params=(room_number,))
    
    def get_all_rooms_with_details(self):
        query = """
        SELECT r.room_number, r.room_type, r.capacity, rd.room_price,
               GROUP_CONCAT(a.amenity SEPARATOR ', ') as amenities
        FROM room r 
        LEFT JOIN room_details rd ON r.room_type = rd.room_type 
        LEFT JOIN room_amenities ra ON r.room_number = ra.room_number
        LEFT JOIN amenity a ON ra.amenity_id = a.amenity_id
        GROUP BY r.room_number
        ORDER BY r.room_number
        """
        return self.db.execute_query(query, fetch=True)
    
    def create_room(self, room_type, capacity):
        return self.insert(['room_type', 'capacity'], [room_type, capacity])
    
    def get_last_room_number(self):
        query = "SELECT room_number FROM room ORDER BY room_number DESC LIMIT 1"
        result = self.db.execute_query(query, fetch=True)
        return result[0][0] if result else None

