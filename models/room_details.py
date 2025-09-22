from models.base_model import BaseModel

class RoomDetails(BaseModel):
    def get_table_name(self):
        return 'room_details'
    
    def get_room_types(self):
        return self.select_all()