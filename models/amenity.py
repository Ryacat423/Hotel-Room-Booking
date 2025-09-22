from models.base_model import BaseModel

class Amenity(BaseModel):
    def get_table_name(self):
        return 'amenity'
    
    def get_all_amenities(self):
        return self.select_all()
    
    def create_amenity(self, amenity_name):
        return self.insert(['amenity'], [amenity_name])
    
    def update_amenity(self, amenity_id, amenity_name):
        return self.update(['amenity'], [amenity_name], 'amenity_id', amenity_id)
    
    def delete_amenity(self, amenity_id):
        return self.delete('amenity_id', amenity_id)

