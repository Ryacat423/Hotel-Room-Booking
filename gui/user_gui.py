import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, date
from services.booking_service import BookingService

class UserGUI:
    def __init__(self, root, return_callback):
        self.root = root
        self.return_callback = return_callback
        self.booking_service = BookingService()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_menu(self):
        self.clear_window()
        
        menu_frame = tk.Frame(self.root, bg='#2c3e50')
        menu_frame.pack(expand=True)
        
        title = tk.Label(menu_frame, text="CUSTOMER MENU", 
                        font=('Arial', 20, 'bold'), bg='#2c3e50', fg='white')
        title.pack(pady=30)
        
        buttons = [
            ("View Available Rooms", self.view_available_rooms),
            ("Make a Booking", self.make_booking),
            ("View My Bookings", self.view_my_bookings),
            ("Back to Main Menu", self.return_callback)
        ]
        
        for text, command in buttons:
            tk.Button(menu_frame, text=text, font=('Arial', 14),
                     bg='#3498db' if text != "Back to Main Menu" else '#95a5a6',
                     fg='white', width=25, height=2,
                     command=command).pack(pady=10)
    
    def view_available_rooms(self):
        self.clear_window()
        
        frame = tk.Frame(self.root, bg='#ecf0f1')
        frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title = tk.Label(frame, text="AVAILABLE ROOMS", 
                        font=('Arial', 18, 'bold'), bg='#ecf0f1')
        title.pack(pady=10)
        
        tree_frame = tk.Frame(frame, bg='#ecf0f1')
        tree_frame.pack(expand=True, fill='both', pady=10)
        
        columns = ('Room #', 'Type', 'Capacity', 'Price', 'Amenities')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        widths = [80, 120, 100, 100, 350]
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')
        
        rooms = self.booking_service.get_all_rooms()
        for room in rooms:
            amenities = room[4] if room[4] else 'None'
            tree.insert('', 'end', values=(room[0], room[1], room[2], 
                                          f"{room[3]:.2f}" if room[3] else "N/A", 
                                          amenities))
        
        tk.Button(frame, text="Back to Customer Menu", font=('Arial', 12),
                 bg='#95a5a6', fg='white', width=20,
                 command=self.show_menu).pack(pady=10)
    
    def make_booking(self):
        self.clear_window()
        
        frame = tk.Frame(self.root, bg='#ecf0f1')
        frame.pack(expand=True, padx=40, pady=40)
        
        title = tk.Label(frame, text="MAKE A BOOKING", 
                        font=('Arial', 18, 'bold'), bg='#ecf0f1')
        title.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Contact
        tk.Label(frame, text="Contact Number:", bg='#ecf0f1', font=('Arial', 11)).grid(row=1, column=0, sticky='e', padx=10, pady=5)
        contact_entry = tk.Entry(frame, font=('Arial', 11), width=30)
        contact_entry.grid(row=1, column=1, pady=5)
        
        # Guest info frame (initially hidden)
        guest_frame = tk.Frame(frame, bg='#ecf0f1')
        guest_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        tk.Label(guest_frame, text="First Name:", bg='#ecf0f1', font=('Arial', 11)).grid(row=0, column=0, sticky='e', padx=10, pady=5)
        firstname_entry = tk.Entry(guest_frame, font=('Arial', 11), width=30)
        firstname_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(guest_frame, text="Last Name:", bg='#ecf0f1', font=('Arial', 11)).grid(row=1, column=0, sticky='e', padx=10, pady=5)
        lastname_entry = tk.Entry(guest_frame, font=('Arial', 11), width=30)
        lastname_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(guest_frame, text="Middle Name:", bg='#ecf0f1', font=('Arial', 11)).grid(row=2, column=0, sticky='e', padx=10, pady=5)
        middlename_entry = tk.Entry(guest_frame, font=('Arial', 11), width=30)
        middlename_entry.grid(row=2, column=1, pady=5)
        
        tk.Label(guest_frame, text="Gender:", bg='#ecf0f1', font=('Arial', 11)).grid(row=3, column=0, sticky='e', padx=10, pady=5)
        gender_var = tk.StringVar(value='M')
        gender_frame_inner = tk.Frame(guest_frame, bg='#ecf0f1')
        gender_frame_inner.grid(row=3, column=1, pady=5, sticky='w')
        tk.Radiobutton(gender_frame_inner, text='Male', variable=gender_var, value='M', bg='#ecf0f1').pack(side='left', padx=5)
        tk.Radiobutton(gender_frame_inner, text='Female', variable=gender_var, value='F', bg='#ecf0f1').pack(side='left', padx=5)
        
        guest_frame.grid_remove()
        
        # Booking dates
        tk.Label(frame, text="Check-in Date (YYYY-MM-DD):", bg='#ecf0f1', font=('Arial', 11)).grid(row=3, column=0, sticky='e', padx=10, pady=5)
        checkin_entry = tk.Entry(frame, font=('Arial', 11), width=30)
        checkin_entry.grid(row=3, column=1, pady=5)
        
        tk.Label(frame, text="Check-out Date (YYYY-MM-DD):", bg='#ecf0f1', font=('Arial', 11)).grid(row=4, column=0, sticky='e', padx=10, pady=5)
        checkout_entry = tk.Entry(frame, font=('Arial', 11), width=30)
        checkout_entry.grid(row=4, column=1, pady=5)
        
        # Room selection
        tk.Label(frame, text="Room Number:", bg='#ecf0f1', font=('Arial', 11)).grid(row=5, column=0, sticky='e', padx=10, pady=5)
        room_entry = tk.Entry(frame, font=('Arial', 11), width=30)
        room_entry.grid(row=5, column=1, pady=5)
        
        def check_guest():
            contact = contact_entry.get()
            if not contact:
                messagebox.showwarning("Warning", "Please enter contact number")
                return
            
            existing = self.booking_service.find_guest_by_contact(contact)
            if existing:
                messagebox.showinfo("Welcome Back", f"Welcome back, {existing[0][1]} {existing[0][2]}!")
                guest_frame.grid_remove()
            else:
                messagebox.showinfo("New Guest", "Please fill in your details")
                guest_frame.grid()
        
        def submit_booking():
            contact = contact_entry.get()
            if not contact:
                messagebox.showwarning("Warning", "Please enter contact number")
                return
            
            # Get or create guest
            existing = self.booking_service.find_guest_by_contact(contact)
            if existing:
                guest_id = existing[0][0]
            else:
                firstname = firstname_entry.get()
                lastname = lastname_entry.get()
                middlename = middlename_entry.get()
                gender = gender_var.get()
                
                if not firstname or not lastname:
                    messagebox.showwarning("Warning", "First name and last name are required")
                    return
                
                guest_id = self.booking_service.create_guest(firstname, lastname, middlename, gender, contact)
                if not guest_id:
                    messagebox.showerror("Error", "Failed to create guest")
                    return
            
            # Validate dates
            try:
                checkin = datetime.strptime(checkin_entry.get(), "%Y-%m-%d").date()
                checkout = datetime.strptime(checkout_entry.get(), "%Y-%m-%d").date()
                
                if checkin >= checkout:
                    messagebox.showerror("Error", "Check-out must be after check-in")
                    return
                
                if checkin < date.today():
                    messagebox.showerror("Error", "Check-in cannot be in the past")
                    return
                
                room_number = int(room_entry.get())
                
                # Check availability
                rooms = self.booking_service.get_available_rooms_with_status(checkin, checkout)
                available = [r for r in rooms if r[4] == 'Available' and r[0] == room_number]
                
                if not available:
                    messagebox.showerror("Error", "Room not available for selected dates")
                    return
                
                # Calculate cost
                nights = (checkout - checkin).days
                room_price = available[0][3]
                total = room_price * nights if room_price else 0
                
                # Confirm
                confirm_msg = f"Room: {room_number}\nCheck-in: {checkin}\nCheck-out: {checkout}\nNights: {nights}\nTotal: {total:.2f}\n\nConfirm booking?"
                if not messagebox.askyesno("Confirm Booking", confirm_msg):
                    return
                
                # Create booking
                booking_id = self.booking_service.create_booking(
                    room_number, guest_id,
                    datetime.combine(checkin, datetime.min.time()),
                    datetime.combine(checkout, datetime.min.time())
                )
                
                if booking_id:
                    messagebox.showinfo("Success", f"Booking confirmed!\nBooking ID: {booking_id}\nTotal: {total:.2f}")
                    self.show_menu()
                else:
                    messagebox.showerror("Error", "Failed to create booking")
                    
            except ValueError as e:
                messagebox.showerror("Error", "Invalid date format or room number")
            except Exception as e:
                messagebox.showerror("Error", f"Booking error: {str(e)}")
        
        btn_frame = tk.Frame(frame, bg='#ecf0f1')
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="Check Guest", font=('Arial', 11),
                 bg='#f39c12', fg='white', width=15,
                 command=check_guest).pack(side='left', padx=10)
        
        tk.Button(btn_frame, text="View Available Rooms", font=('Arial', 11),
                 bg='#3498db', fg='white', width=18,
                 command=self.show_available_rooms_dialog).pack(side='left', padx=10)
        
        tk.Button(btn_frame, text="Submit Booking", font=('Arial', 11),
                 bg='#27ae60', fg='white', width=15,
                 command=submit_booking).pack(side='left', padx=10)
        
        tk.Button(frame, text="Back to Customer Menu", font=('Arial', 12),
                 bg='#95a5a6', fg='white', width=20,
                 command=self.show_menu).grid(row=7, column=0, columnspan=2, pady=10)
    
    def show_available_rooms_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Available Rooms")
        dialog.geometry("800x400")
        
        frame = tk.Frame(dialog)
        frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        columns = ('Room #', 'Type', 'Capacity', 'Price', 'Amenities')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        widths = [80, 120, 100, 100, 350]
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')
        
        rooms = self.booking_service.get_all_rooms()
        for room in rooms:
            amenities = room[4] if room[4] else 'None'
            tree.insert('', 'end', values=(room[0], room[1], room[2], 
                                          f"{room[3]:.2f}" if room[3] else "N/A", 
                                          amenities))
    
    def view_my_bookings(self):
        contact = simpledialog.askstring("View Bookings", "Enter your contact number:")
        if not contact:
            return
        
        guest = self.booking_service.find_guest_by_contact(contact)
        if not guest:
            messagebox.showerror("Error", "No guest found with this contact")
            return
        
        guest_id = guest[0][0]
        bookings = self.booking_service.get_guest_bookings(guest_id)
        
        if not bookings:
            messagebox.showinfo("No Bookings", "No bookings found for this contact")
            return
        
        # Show bookings in dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("My Bookings")
        dialog.geometry("700x400")
        
        frame = tk.Frame(dialog, bg='#ecf0f1')
        frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title = tk.Label(frame, text="YOUR BOOKINGS", 
                        font=('Arial', 16, 'bold'), bg='#ecf0f1')
        title.pack(pady=10)
        
        columns = ('Booking ID', 'Room #', 'Check-in', 'Check-out', 'Status')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')
        
        for booking in bookings:
            checkin = booking[4].strftime('%Y-%m-%d') if hasattr(booking[4], 'strftime') else booking[4]
            checkout = booking[5].strftime('%Y-%m-%d') if hasattr(booking[5], 'strftime') else booking[5]
            tree.insert('', 'end', values=(booking[0], booking[2], checkin, checkout, booking[6]))
        
        tk.Button(frame, text="Close", font=('Arial', 11),
                 bg='#95a5a6', fg='white', width=15,
                 command=dialog.destroy).pack(pady=10)