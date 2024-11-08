import tkinter as tk
from tkinter import ttk
from datetime import datetime
import time
import threading
from bin.lib.ApiAllTicket import ApiAllTicket
from bin.lib.ApiFindById import ApiFindById

# สร้างหน้าต่างหลัก
root = tk.Tk()

root.title("BOT TICKET")
root.geometry("500x600")
root.configure(bg="#f0f0f0")
root.resizable(False, False)

# กำหนดฟอนต์พื้นฐานและสี
font = ("Helvetica", 10)
header_font = ("Helvetica", 18, "bold")
button_font = ("Helvetica", 12, "bold")
bg_color = "#f0f0f0"
text_color = "#333333"

# ส่วนหัว
header_label = tk.Label(root, text="All Ticket", font=header_font, fg=text_color, bg=bg_color)
header_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

# ฟิลด์สำหรับใส่ Token
tk.Label(root, text="Token", font=font, fg=text_color, bg=bg_color).grid(row=1, column=0, sticky="e", padx=10, pady=5)
token_entry = tk.Entry(root, width=30, font=font, show="*")
token_entry.grid(row=1, column=1, sticky="w", padx=10)

# ฟิลด์สำหรับ Name
tk.Label(root, text="Name", font=font, fg=text_color, bg=bg_color).grid(row=2, column=0, sticky="e", padx=10, pady=5)
name_entry = tk.Entry(root, width=30, font=font)
name_entry.grid(row=2, column=1, sticky="w", padx=10)

# ฟิลด์สำหรับ Zone
tk.Label(root, text="Zone", font=font, fg=text_color, bg=bg_color).grid(row=3, column=0, sticky="e", padx=10, pady=5)
zone_entry = tk.Entry(root, width=10, font=font)
zone_entry.grid(row=3, column=1, sticky="w", padx=10)

# ฟิลด์สำหรับ Date
tk.Label(root, text="Date (R1 format)", font=font, fg=text_color, bg=bg_color).grid(row=4, column=0, sticky="e", padx=10, pady=5)
date_entry = tk.Entry(root, width=10, font=font)
date_entry.grid(row=4, column=1, sticky="w", padx=10)

# ฟิลด์สำหรับ Total Ticket
tk.Label(root, text="Total Ticket", font=font, fg=text_color, bg=bg_color).grid(row=5, column=0, sticky="e", padx=10, pady=5)
ticket_number = ttk.Combobox(root, values=["1", "2", "3", "4"], font=font, width=5)
ticket_number.grid(row=5, column=1, sticky="w", padx=10)
ticket_number.insert(0, "1")

# ฟิลด์สำหรับ Time และตั้งเวลา
tk.Label(root, text="Time", font=font, fg=text_color, bg=bg_color).grid(row=6, column=0, sticky="e", padx=10, pady=5)
time_entry = tk.Entry(root, width=10, font=font)
time_entry.grid(row=6, column=1, sticky="w", padx=10)
time_entry.insert(0, datetime.now().strftime("%H:%M:%S"))
set_time_var = tk.BooleanVar()
set_time_checkbox = tk.Checkbutton(root, text="Set timer", variable=set_time_var, font=font, fg=text_color, bg=bg_color)
set_time_checkbox.grid(row=6, column=1)

# ฟังก์ชันเพื่อเริ่มต้นการทำงานตามเวลาที่ตั้งไว้
def start_at_scheduled_time():
    if set_time_var.get():  # ตรวจสอบว่าติ๊ก "ตั้งเวลา" หรือไม่
        status_text.insert("2.0", "bot timer start.\n")
        target_time_str = time_entry.get()  # เวลาเป้าหมายในฟอร์แมต HH:MM:SS
        try:
            target_time = datetime.strptime(target_time_str, "%H:%M:%S").time()
        except ValueError:
            status_text.insert("1.0", "Invalid time format. Please use HH:MM:SS.\n")
            return

        while True:
            current_time = datetime.now().time()
            if current_time >= target_time:
                start_action()  # เรียกฟังก์ชัน start_action เมื่อถึงเวลาที่กำหนด
                break
            time.sleep(1)  # รอ 1 วินาทีแล้วเช็คใหม่อีกครั้ง

# ฟังก์ชันสำหรับปุ่ม Start
def on_start_button_click():
    # ถ้าติ๊กที่ "ตั้งเวลา" ให้ใช้ฟังก์ชันตามเวลาที่ตั้งไว้
    if set_time_var.get():
        threading.Thread(target=start_at_scheduled_time).start()
    else:
        start_action()  # ถ้าไม่ได้ตั้งเวลา ให้ทำงานทันที

# ฟังก์ชันสำหรับเริ่มทำงาน
def start_action():
    token = token_entry.get()
    name = name_entry.get()
    zone_id = zone_entry.get()
    round_id = date_entry.get()
    tickets = int(ticket_number.get())
    time_set = time_entry.get()

    # เรียกใช้ APIFindById เพื่อดึง event_id
    api_find_by_id = ApiFindById(token,name)
    event_id = api_find_by_id.get_event_id(name)

    if event_id:
        # ใช้ event_id ที่ได้มาไปทำงานกับ ApiAllTicket
        api_all_ticket = ApiAllTicket(token, name)
        if zone_id == "REG":
            number_uuid = api_all_ticket.handler_reserve_festival(event_id, zone_id, round_id, int(tickets))
            status_text.insert("2.0", f"Reservation UUID: {number_uuid}. \n success.... \n")
        else:
            # เรียกใช้ฟังก์ชันจาก ApiAllTicket
            available_seats = api_all_ticket.get_seats(event_id, round_id, zone_id, int(tickets))
            print(available_seats)
            # ทำการจองที่นั่ง
            number_uuid = api_all_ticket.handler_reserve(event_id, zone_id, round_id, available_seats)
            status_text.insert("2.0", f"Reservation UUID: {number_uuid}. \n success.... \n")

    else:
        status_text.insert("2.0", "Failed to retrieve event ID.\n")

# ปุ่ม Start และ Cancel
button_frame = tk.Frame(root, bg=bg_color)
button_frame.grid(row=9, column=0, columnspan=2, pady=(20, 10))

start_button = tk.Button(button_frame, text="START", font=button_font, bg="blue", fg="white", width=12, command=on_start_button_click)
start_button.pack(side="left", padx=10)

cancel_button = tk.Button(button_frame, text="Cancel", font=button_font, bg="red", fg="white", width=12)
cancel_button.pack(side="left", padx=10)

# ช่องแสดงสถานะ
status_text = tk.Text(root, height=8, font=font, wrap="word")
status_text.grid(row=10, column=0, columnspan=2, pady=(10, 20), padx=10, sticky="ew")
status_text.insert("1.0", "Bot start... \n")

# กำหนด column weight ให้ช่องแสดงสถานะและปุ่มอยู่ตรงกลาง
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# เริ่มต้นการทำงานของ GUI
root.mainloop()