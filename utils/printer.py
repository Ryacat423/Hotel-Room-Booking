import serial
import logging
from datetime import datetime
from config.printer_config import PRINTER_CONFIG

logger = logging.getLogger(__name__)

class ThermalPrinter:
    def __init__(self):
        self.config = PRINTER_CONFIG
        self.ser = None
    
    def connect(self):
        """Connect to thermal printer"""
        if not self.config['enabled']:
            logger.info("Printer disabled in configuration")
            return False
            
        try:
            self.ser = serial.Serial(
                self.config['port'], 
                self.config['baudrate'], 
                timeout=self.config['timeout']
            )

            self.ser.write(b'\x1B\x40')
            logger.info(f"Connected to thermal printer on {self.config['port']}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to printer: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from thermal printer"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            logger.info("Disconnected from thermal printer")
    
    def print_text(self, text):
        """Print text to thermal printer"""
        if not self.config['enabled']:
            logger.info("Print skipped - printer disabled")
            return True
            
        if not self.ser or not self.ser.is_open:
            if not self.connect():
                return False
        
        try:
            # Encode text and send to printer
            self.ser.write(text.encode('utf-8'))
            return True
        except Exception as e:
            logger.error(f"Failed to print: {e}")
            return False
    
    def print_receipt(self, booking_data):
        """Print booking receipt"""
        receipt = self._generate_booking_receipt(booking_data)
        return self.print_text(receipt)
    
    def print_admin_report(self, report_data, report_type):
        """Print admin reports"""
        if report_type == "bookings":
            report = self._generate_bookings_report(report_data)
        elif report_type == "rooms":
            report = self._generate_rooms_report(report_data)
        else:
            report = "Unknown report type\n"
        
        return self.print_text(report)
    
    def _generate_booking_receipt(self, booking_data):
        """Generate formatted booking receipt"""
        receipt = []
        receipt.append("=" * 32)
        receipt.append("    HOTEL BOOKING RECEIPT")
        receipt.append("=" * 32)
        receipt.append("")
        
        # Booking details
        receipt.append(f"Booking ID: {booking_data['booking_id']}")
        receipt.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        receipt.append("")
        
        # Guest details
        receipt.append("GUEST INFORMATION:")
        receipt.append("-" * 20)
        receipt.append(f"Name: {booking_data['guest_name']}")
        receipt.append(f"Contact: {booking_data['contact']}")
        receipt.append("")
        
        # Room details
        receipt.append("ROOM INFORMATION:")
        receipt.append("-" * 20)
        receipt.append(f"Room Number: {booking_data['room_number']}")
        receipt.append(f"Room Type: {booking_data['room_type']}")
        receipt.append(f"Capacity: {booking_data['capacity']} persons")
        receipt.append("")
        
        # Stay details
        receipt.append("STAY DETAILS:")
        receipt.append("-" * 20)
        receipt.append(f"Check-in: {booking_data['checkin_date']}")
        receipt.append(f"Check-out: {booking_data['checkout_date']}")
        receipt.append(f"Nights: {booking_data['nights']}")
        receipt.append("")
        
        # Billing
        receipt.append("BILLING:")
        receipt.append("-" * 20)
        receipt.append(f"Rate/Night: ${booking_data['rate']:.2f}")
        receipt.append(f"Total Amount: ${booking_data['total']:.2f}")
        receipt.append(f"Status: {booking_data['status'].upper()}")
        receipt.append("")
        
        receipt.append("=" * 32)
        receipt.append("Thank you for choosing our hotel!")
        receipt.append("Have a pleasant stay!")
        receipt.append("=" * 32)
        receipt.append("")
        receipt.append("")
        receipt.append("")  # Feed paper
        
        return "\n".join(receipt)
    
    def _generate_bookings_report(self, bookings):
        """Generate bookings report"""
        report = []
        report.append("=" * 32)
        report.append("    BOOKINGS REPORT")
        report.append("=" * 32)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("")
        
        if not bookings:
            report.append("No bookings found.")
        else:
            for i, booking in enumerate(bookings, 1):
                report.append(f"{i}. Booking ID: {booking[0]}")
                report.append(f"   Room: {booking[1]}")
                report.append(f"   Check-in: {booking[3]}")
                report.append(f"   Status: {booking[5]}")
                report.append("")
        
        report.append("=" * 32)
        report.append("")
        report.append("")
        
        return "\n".join(report)
    
    def _generate_rooms_report(self, rooms):
        """Generate rooms report"""
        report = []
        report.append("=" * 32)
        report.append("    ROOMS REPORT")
        report.append("=" * 32)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("")
        
        if not rooms:
            report.append("No rooms found.")
        else:
            for i, room in enumerate(rooms, 1):
                report.append(f"{i}. Room {room[0]}")
                report.append(f"   Type: {room[1]}")
                report.append(f"   Capacity: {room[2]} persons")
                report.append("")
        
        report.append("=" * 32)
        report.append("")
        report.append("")
        
        return "\n".join(report)
    
    def test_printer(self):
        """Test printer connectivity"""
        test_text = []
        test_text.append("=" * 32)
        test_text.append("    PRINTER TEST")
        test_text.append("=" * 32)
        test_text.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        test_text.append("")
        test_text.append("If you can read this,")
        test_text.append("the printer is working!")
        test_text.append("")
        test_text.append("=" * 32)
        test_text.append("")
        test_text.append("")
        
        return self.print_text("\n".join(test_text))