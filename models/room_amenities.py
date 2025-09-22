from models.base_model import BaseModel

class RoomAmenities(BaseModel):
    def get_table_name(self):
        return 'room_amenities'
    
    def assign_amenity_to_room(self, room_number, amenity_id):
        return self.insert(['room_number', 'amenity_id'], [room_number, amenity_id])
    
    def remove_amenity_from_room(self, room_number, amenity_id):
        query = "DELETE FROM room_amenities WHERE room_number = %s AND amenity_id = %s"
        return self.db.execute_query(query, params=(room_number, amenity_id))
    
    def get_room_amenities(self, room_number):
        query = """
        SELECT a.amenity_id, a.amenity 
        FROM amenity a
        JOIN room_amenities ra ON a.amenity_id = ra.amenity_id
        WHERE ra.room_number = %s
        """
        return self.db.execute_query(query, fetch=True, params=(room_number,))
    
    def clear_room_amenities(self, room_number):
        query = "DELETE FROM room_amenities WHERE room_number = %s"
        return self.db.execute_query(query, params=(room_number,))

