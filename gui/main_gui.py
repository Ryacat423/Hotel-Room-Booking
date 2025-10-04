
import tkinter as tk
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from gui.admin_gui import AdminGUI
from gui.user_gui import UserGUI

class HotelBookingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hotel Room Booking System")
        self.root.geometry("900x600")
        self.root.configure(bg='#2c3e50')
        
        # Initialize GUI modules
        self.admin_gui = AdminGUI(self.root, self.show_main_menu)
        self.user_gui = UserGUI(self.root, self.show_main_menu)
        
        self.show_main_menu()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_main_menu(self):
        self.clear_window()
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        # Title
        title = tk.Label(main_frame, text="HOTEL ROOM BOOKING SYSTEM", 
                        font=('Arial', 24, 'bold'), bg='#2c3e50', fg='white')
        title.pack(pady=30)
        
        # Button frame
        btn_frame = tk.Frame(main_frame, bg='#2c3e50')
        btn_frame.pack(expand=True)
        
        # Admin button
        admin_btn = tk.Button(btn_frame, text="Admin Login", font=('Arial', 16),
                             bg='#e74c3c', fg='white', width=20, height=2,
                             command=self.admin_gui.show_login)
        admin_btn.pack(pady=15)
        
        # Customer button
        customer_btn = tk.Button(btn_frame, text="Customer Booking", font=('Arial', 16),
                                bg='#3498db', fg='white', width=20, height=2,
                                command=self.user_gui.show_menu)
        customer_btn.pack(pady=15)
        
        # Exit button
        exit_btn = tk.Button(btn_frame, text="Exit", font=('Arial', 16),
                           bg='#95a5a6', fg='white', width=20, height=2,
                           command=self.root.quit)
        exit_btn.pack(pady=15)
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = HotelBookingApp()
    app.run()