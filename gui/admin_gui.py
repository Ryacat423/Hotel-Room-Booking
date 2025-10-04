import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from services.admin_service import AdminService

class AdminGUI:
    def __init__(self, root, return_callback):
        self.root = root
        self.return_callback = return_callback
        self.admin_service = AdminService()
        self.current_tree = None
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login(self):
        self.clear_window()
        
        login_frame = tk.Frame(self.root, bg='#2c3e50')
        login_frame.pack(expand=True)
        
        title = tk.Label(login_frame, text="ADMIN LOGIN", 
                        font=('Arial', 20, 'bold'), bg='#2c3e50', fg='white')
        title.pack(pady=20)
        
        tk.Label(login_frame, text="Username:", font=('Arial', 12),
                bg='#2c3e50', fg='white').pack(pady=5)
        username_entry = tk.Entry(login_frame, font=('Arial', 12), width=25)
        username_entry.pack(pady=5)
        
        tk.Label(login_frame, text="Password:", font=('Arial', 12),
                bg='#2c3e50', fg='white').pack(pady=5)
        password_entry = tk.Entry(login_frame, font=('Arial', 12), width=25, show='*')
        password_entry.pack(pady=5)
        
        def login():
            username = username_entry.get()
            password = password_entry.get()
            
            if self.admin_service.authenticate(username, password):
                messagebox.showinfo("Success", "Login successful!")
                self.show_menu()
            else:
                messagebox.showerror("Error", "Invalid credentials!")
        
        btn_frame = tk.Frame(login_frame, bg='#2c3e50')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Login", font=('Arial', 12),
                 bg='#27ae60', fg='white', width=12,
                 command=login).pack(side='left', padx=10)
        
        tk.Button(btn_frame, text="Back", font=('Arial', 12),
                 bg='#95a5a6', fg='white', width=12,
                 command=self.return_callback).pack(side='left', padx=10)
    
    def show_menu(self):
        self.clear_window()
        
        menu_frame = tk.Frame(self.root, bg='#2c3e50')
        menu_frame.pack(expand=True)
        
        title = tk.Label(menu_frame, text="ADMIN MENU", 
                        font=('Arial', 20, 'bold'), bg='#2c3e50', fg='white')
        title.pack(pady=30)
        
        buttons = [
            ("Amenity Management", self.show_amenity_management),
            ("Room Details Management", self.show_room_details_management),
            ("Room Management", self.show_room_management),
            ("Booking Management", self.show_booking_management),
            ("Logout", self.return_callback)
        ]
        
        for text, command in buttons:
            tk.Button(menu_frame, text=text, font=('Arial', 14),
                     bg='#3498db' if text != "Logout" else '#e74c3c',
                     fg='white', width=25, height=2,
                     command=command).pack(pady=10)
    
    def show_amenity_management(self):
        self.clear_window()
        
        frame = tk.Frame(self.root, bg='#ecf0f1')
        frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title = tk.Label(frame, text="AMENITY MANAGEMENT", 
                        font=('Arial', 18, 'bold'), bg='#ecf0f1')
        title.pack(pady=10)
        
        btn_frame = tk.Frame(frame, bg='#ecf0f1')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Add Amenity", font=('Arial', 11),
                 bg='#27ae60', fg='white', width=15,
                 command=self.add_amenity).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Update Amenity", font=('Arial', 11),
                 bg='#f39c12', fg='white', width=15,
                 command=self.update_amenity).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Delete Amenity", font=('Arial', 11),
                 bg='#e74c3c', fg='white', width=15,
                 command=self.delete_amenity).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Refresh", font=('Arial', 11),
                 bg='#3498db', fg='white', width=15,
                 command=lambda: self.load_amenities(tree)).pack(side='left', padx=5)
        
        tree_frame = tk.Frame(frame, bg='#ecf0f1')
        tree_frame.pack(expand=True, fill='both', pady=10)
        
        columns = ('ID', 'Amenity')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')
        
        self.load_amenities(tree)
        
        tk.Button(frame, text="Back to Admin Menu", font=('Arial', 12),
                 bg='#95a5a6', fg='white', width=20,
                 command=self.show_menu).pack(pady=10)
        
        self.current_tree = tree
    
    def load_amenities(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        
        amenities = self.admin_service.get_all_amenities()
        for amenity in amenities:
            tree.insert('', 'end', values=amenity)
    
    def add_amenity(self):
        name = simpledialog.askstring("Add Amenity", "Enter amenity name:")
        if name:
            if self.admin_service.add_amenity(name):
                messagebox.showinfo("Success", "Amenity added successfully!")
                self.load_amenities(self.current_tree)
            else:
                messagebox.showerror("Error", "Failed to add amenity")
    
    def update_amenity(self):
        selected = self.current_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an amenity")
            return
        
        values = self.current_tree.item(selected[0])['values']
        amenity_id = values[0]
        
        new_name = simpledialog.askstring("Update Amenity", 
                                         "Enter new amenity name:",
                                         initialvalue=values[1])
        if new_name:
            if self.admin_service.update_amenity(amenity_id, new_name):
                messagebox.showinfo("Success", "Amenity updated successfully!")
                self.load_amenities(self.current_tree)
            else:
                messagebox.showerror("Error", "Failed to update amenity")
    
    def delete_amenity(self):
        selected = self.current_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an amenity")
            return
        
        values = self.current_tree.item(selected[0])['values']
        amenity_id = values[0]
        
        if messagebox.askyesno("Confirm", f"Delete amenity '{values[1]}'?"):
            if self.admin_service.delete_amenity(amenity_id):
                messagebox.showinfo("Success", "Amenity deleted successfully!")
                self.load_amenities(self.current_tree)
            else:
                messagebox.showerror("Error", "Failed to delete amenity")
    
    def show_room_details_management(self):
        self.clear_window()
        
        frame = tk.Frame(self.root, bg='#ecf0f1')
        frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title = tk.Label(frame, text="ROOM DETAILS MANAGEMENT", 
                        font=('Arial', 18, 'bold'), bg='#ecf0f1')
        title.pack(pady=10)
        
        btn_frame = tk.Frame(frame, bg='#ecf0f1')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Add Room Detail", font=('Arial', 11),
                 bg='#27ae60', fg='white', width=15,
                 command=self.add_room_detail).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Update Price", font=('Arial', 11),
                 bg='#f39c12', fg='white', width=15,
                 command=self.update_room_detail).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Delete Room Detail", font=('Arial', 11),
                 bg='#e74c3c', fg='white', width=15,
                 command=self.delete_room_detail).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Refresh", font=('Arial', 11),
                 bg='#3498db', fg='white', width=15,
                 command=lambda: self.load_room_details(tree)).pack(side='left', padx=5)
        
        tree_frame = tk.Frame(frame, bg='#ecf0f1')
        tree_frame.pack(expand=True, fill='both', pady=10)
        
        columns = ('Room Type', 'Price')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=250)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')
        
        self.load_room_details(tree)
        
        tk.Button(frame, text="Back to Admin Menu", font=('Arial', 12),
                 bg='#95a5a6', fg='white', width=20,
                 command=self.show_menu).pack(pady=10)
        
        self.current_tree = tree
    
    def load_room_details(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        
        details = self.admin_service.get_all_room_details()
        for detail in details:
            tree.insert('', 'end', values=(detail[0], f"{detail[1]:.2f}"))
    
    def add_room_detail(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Room Detail")
        dialog.geometry("300x200")
        
        tk.Label(dialog, text="Room Type:").pack(pady=5)
        type_entry = tk.Entry(dialog, width=30)
        type_entry.pack(pady=5)
        
        tk.Label(dialog, text="Price:").pack(pady=5)
        price_entry = tk.Entry(dialog, width=30)
        price_entry.pack(pady=5)
        
        def save():
            room_type = type_entry.get()
            try:
                price = float(price_entry.get())
                if self.admin_service.add_room_detail(room_type, price):
                    messagebox.showinfo("Success", "Room detail added!")
                    self.load_room_details(self.current_tree)
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to add room detail")
            except ValueError:
                messagebox.showerror("Error", "Invalid price format")
        
        tk.Button(dialog, text="Save", command=save).pack(pady=10)
    
    def update_room_detail(self):
        selected = self.current_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a room detail")
            return
        
        values = self.current_tree.item(selected[0])['values']
        room_type = values[0]
        
        new_price = simpledialog.askfloat("Update Price", 
                                         "Enter new price:",
                                         initialvalue=float(values[1]))
        if new_price is not None:
            if self.admin_service.update_room_detail(room_type, new_price):
                messagebox.showinfo("Success", "Price updated successfully!")
                self.load_room_details(self.current_tree)
            else:
                messagebox.showerror("Error", "Failed to update price")
    
    def delete_room_detail(self):
        selected = self.current_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a room detail")
            return
        
        values = self.current_tree.item(selected[0])['values']
        room_type = values[0]
        
        if messagebox.askyesno("Confirm", f"Delete room type '{room_type}'?"):
            if self.admin_service.delete_room_detail(room_type):
                messagebox.showinfo("Success", "Room detail deleted!")
                self.load_room_details(self.current_tree)
            else:
                messagebox.showerror("Error", "Failed to delete room detail")
    
    def show_room_management(self):
        self.clear_window()
        
        frame = tk.Frame(self.root, bg='#ecf0f1')
        frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title = tk.Label(frame, text="ROOM MANAGEMENT", 
                        font=('Arial', 18, 'bold'), bg='#ecf0f1')
        title.pack(pady=10)
        
        btn_frame = tk.Frame(frame, bg='#ecf0f1')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Add Room", font=('Arial', 11),
                 bg='#27ae60', fg='white', width=12,
                 command=self.add_room).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Delete Room", font=('Arial', 11),
                 bg='#e74c3c', fg='white', width=12,
                 command=self.delete_room).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Refresh", font=('Arial', 11),
                 bg='#3498db', fg='white', width=12,
                 command=lambda: self.load_rooms(tree)).pack(side='left', padx=5)
        
        tree_frame = tk.Frame(frame, bg='#ecf0f1')
        tree_frame.pack(expand=True, fill='both', pady=10)
        
        columns = ('Room #', 'Type', 'Capacity', 'Price', 'Amenities')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        widths = [80, 120, 100, 100, 300]
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')
        
        self.load_rooms(tree)
        
        tk.Button(frame, text="Back to Admin Menu", font=('Arial', 12),
                 bg='#95a5a6', fg='white', width=20,
                 command=self.show_menu).pack(pady=10)
        
        self.current_tree = tree
    
    def load_rooms(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        
        rooms = self.admin_service.get_all_rooms()
        for room in rooms:
            amenities = room[4] if room[4] else 'None'
            tree.insert('', 'end', values=(room[0], room[1], room[2], 
                                          f"{room[3]:.2f}" if room[3] else "N/A", 
                                          amenities))
    
    def add_room(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Room")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="Room Type:").pack(pady=5)
        type_entry = tk.Entry(dialog, width=30)
        type_entry.pack(pady=5)
        
        tk.Label(dialog, text="Capacity:").pack(pady=5)
        capacity_entry = tk.Entry(dialog, width=30)
        capacity_entry.pack(pady=5)
        
        tk.Label(dialog, text="Amenity IDs (comma-separated):").pack(pady=5)
        amenities_entry = tk.Entry(dialog, width=30)
        amenities_entry.pack(pady=5)
        
        def save():
            room_type = type_entry.get()
            try:
                capacity = int(capacity_entry.get())
                amenities_str = amenities_entry.get().strip()
                amenity_ids = []
                if amenities_str:
                    amenity_ids = [int(x.strip()) for x in amenities_str.split(',')]
                
                if self.admin_service.add_room(room_type, capacity, amenity_ids):
                    messagebox.showinfo("Success", "Room added successfully!")
                    self.load_rooms(self.current_tree)
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to add room")
            except ValueError:
                messagebox.showerror("Error", "Invalid input format")
        
        tk.Button(dialog, text="Save", command=save).pack(pady=10)
    
    def delete_room(self):
        selected = self.current_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a room")
            return
        
        values = self.current_tree.item(selected[0])['values']
        room_number = values[0]
        
        if messagebox.askyesno("Confirm", f"Delete Room {room_number}?"):
            if self.admin_service.delete_room(room_number):
                messagebox.showinfo("Success", "Room deleted successfully!")
                self.load_rooms(self.current_tree)
            else:
                messagebox.showerror("Error", "Failed to delete room")
    
    def show_booking_management(self):
        self.clear_window()
        
        frame = tk.Frame(self.root, bg='#ecf0f1')
        frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title = tk.Label(frame, text="BOOKING MANAGEMENT", 
                        font=('Arial', 18, 'bold'), bg='#ecf0f1')
        title.pack(pady=10)
        
        btn_frame = tk.Frame(frame, bg='#ecf0f1')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Cancel Booking", font=('Arial', 11),
                 bg='#e74c3c', fg='white', width=15,
                 command=self.cancel_booking).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Refresh", font=('Arial', 11),
                 bg='#3498db', fg='white', width=15,
                 command=lambda: self.load_bookings(tree)).pack(side='left', padx=5)
        
        tree_frame = tk.Frame(frame, bg='#ecf0f1')
        tree_frame.pack(expand=True, fill='both', pady=10)
        
        columns = ('Booking ID', 'Guest', 'Room', 'Type', 'Check-in', 'Check-out', 'Status', 'Price')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        widths = [80, 150, 60, 100, 100, 100, 80, 80]
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')
        
        self.load_bookings(tree)
        
        tk.Button(frame, text="Back to Admin Menu", font=('Arial', 12),
                 bg='#95a5a6', fg='white', width=20,
                 command=self.show_menu).pack(pady=10)
        
        self.current_tree = tree
    
    def load_bookings(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        
        bookings = self.admin_service.get_all_bookings()
        for booking in bookings:
            guest_name = f"{booking[1]} {booking[2]}"
            checkin = booking[5].strftime('%Y-%m-%d') if hasattr(booking[5], 'strftime') else booking[5]
            checkout = booking[6].strftime('%Y-%m-%d') if hasattr(booking[6], 'strftime') else booking[6]
            price = f"{booking[8]:.2f}" if booking[8] else "N/A"
            tree.insert('', 'end', values=(booking[0], guest_name, booking[3], 
                                          booking[4], checkin, checkout, 
                                          booking[7], price))
    
    def cancel_booking(self):
        selected = self.current_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a booking")
            return
        
        values = self.current_tree.item(selected[0])['values']
        booking_id = values[0]
        
        if messagebox.askyesno("Confirm", f"Cancel booking ID {booking_id}?"):
            if self.admin_service.cancel_booking(booking_id):
                messagebox.showinfo("Success", "Booking cancelled successfully!")
                self.load_bookings(self.current_tree)
            else:
                messagebox.showerror("Error", "Failed to cancel booking")