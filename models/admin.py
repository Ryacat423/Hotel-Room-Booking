from models.base_model import BaseModel
import hashlib

class Admin(BaseModel):
    def get_table_name(self):
        return 'admin'
    
    def authenticate(self, username, password):
        hashed_password = hashlib.sha1(password.encode()).hexdigest()
        result = self.select_where(['username', 'password'], (username, hashed_password))
        return bool(result)