from models.base_model import BaseModel

class Guest(BaseModel):
    def get_table_name(self):
        return 'guest'
    
    def create_guest(self, firstname, lastname, middlename, gender, contact_info):
        return self.insert(
            ['firstname', 'lastname', 'middlename', 'gender', 'contact_info'],
            (firstname, lastname, middlename, gender, contact_info)
        )
    
    def get_guest_by_contact(self, contact_info):
        return self.select_where(['contact_info'], (contact_info,))
