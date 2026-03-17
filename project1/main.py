import customtkinter as ctk
import calendar
from datetime import datetime

BG_COLOR = "#1c1c1c"
BG_SECONDARY = "#404040"
ACCENT_COLOR = "#3c3cf6"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#94a3b8"
BORDER_COLOR = "#404040"

ctk.set_appearance_mode("dark")

class DatePickerPopup(ctk.CTkToplevel):
    def __init__(self, master, callback, initial_date=None):
        super().__init__(master)
        self.title("Select Date")
        self.geometry("320x350")
        self.configure(fg_color=BG_COLOR)
        self.attributes("-topmost", True)
        self.resizable(False, False)
        self.callback = callback

        if initial_date:
            try:
                dt = datetime.strptime(initial_date, "%Y-%m-%d")
                self.current_year = dt.year
                self.current_month = dt.month
            except ValueError:
                self.current_year = datetime.now().year
                self.current_month = datetime.now().month
        else:
            self.current_year = datetime.now().year
            self.current_month = datetime.now().month

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(self.header_frame, text="<", width=30, fg_color="transparent", hover_color=BG_SECONDARY, command=self.prev_month).pack(side="left", padx=10)
        self.month_lbl = ctk.CTkLabel(self.header_frame, text="", font=("Helvetica", 16, "bold"))
        self.month_lbl.pack(side="left", expand=True)
        ctk.CTkButton(self.header_frame, text=">", width=30, fg_color="transparent", hover_color=BG_SECONDARY, command=self.next_month).pack(side="right", padx=10)

        self.days_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.days_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        for i, day in enumerate(days):
            self.days_frame.columnconfigure(i, weight=1, uniform="col")
            ctk.CTkLabel(self.days_frame, text=day, text_color=TEXT_SECONDARY, font=("Helvetica", 12, "bold")).grid(row=0, column=i)

        self.build_calendar()

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.build_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.build_calendar()

    def build_calendar(self):
        for widget in self.days_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        month_name = calendar.month_name[self.current_month]
        self.month_lbl.configure(text=f"{month_name} {self.current_year}")

        first_weekday, num_days = calendar.monthrange(self.current_year, self.current_month)
        start_col = first_weekday

        day_counter = 1
        for row in range(1, 7):
            self.days_frame.rowconfigure(row, weight=1, uniform="row")
            for col in range(7):
                if (row == 1 and col < start_col) or day_counter > num_days:
                    continue
                
                btn = ctk.CTkButton(
                    self.days_frame, text=str(day_counter), width=30, height=30, 
                    fg_color="transparent", text_color=TEXT_PRIMARY, hover_color=BG_SECONDARY,
                    command=lambda d=day_counter: self.select_date(d)
                )
                btn.grid(row=row, column=col, padx=2, pady=2)
                day_counter += 1

    def select_date(self, day):
        date_str = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
        self.callback(date_str)
        self.destroy()

class UnderlineEntry(ctk.CTkFrame):
    def __init__(self, master, placeholder, icon=None, icon_command=None, readonly=False, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.columnconfigure(0, weight=1)
        
        self.entry = ctk.CTkEntry(
            self, 
            placeholder_text=placeholder,
            fg_color="transparent",
            border_width=0,
            text_color=TEXT_PRIMARY,
            placeholder_text_color=TEXT_SECONDARY,
            font=("Helvetica", 16)
        )
        self.entry.grid(row=0, column=0, sticky="ew", pady=(5, 0))
        
        if readonly:
            self.entry.configure(state="readonly")
        
        if icon:
            if icon_command:
                self.icon_btn = ctk.CTkButton(
                    self, text=icon, width=40, height=30,
                    fg_color="transparent", text_color=ACCENT_COLOR,
                    hover_color=BG_SECONDARY, font=("Helvetica", 20),
                    command=icon_command
                )
                self.icon_btn.grid(row=0, column=1, sticky="e", padx=(0, 0))
            else:
                self.icon_label = ctk.CTkLabel(self, text=icon, text_color=TEXT_SECONDARY, font=("Helvetica", 16))
                self.icon_label.grid(row=0, column=1, sticky="e", padx=(0, 5))
            
        self.line = ctk.CTkFrame(self, height=1, fg_color=BORDER_COLOR)
        self.line.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(2, 0))

    def set_text(self, text):
        current_state = self.entry.cget("state")
        self.entry.configure(state="normal")
        self.entry.delete(0, 'end')
        self.entry.insert(0, text)
        if current_state == "readonly":
            self.entry.configure(state="readonly")

    def get_text(self):
        return self.entry.get()

class MonthView(ctk.CTkFrame):
    def __init__(self, master, switch_to_add, switch_to_details):
        super().__init__(master, fg_color=BG_COLOR)
        self.switch_to_add = switch_to_add
        self.switch_to_details = switch_to_details
        self.calendar_container = None
        
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        
        self.topbar = ctk.CTkFrame(self, height=60, fg_color=BG_COLOR, corner_radius=0)
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)
        ctk.CTkLabel(self.topbar, text="🗓️ EVENT PLANNER", font=("Helvetica", 14, "bold"), text_color=TEXT_SECONDARY).pack(side="left", padx=20)
        
        ctk.CTkButton(
            self.topbar, text="+", width=40, fg_color="transparent", hover_color=BG_SECONDARY,
            text_color=TEXT_PRIMARY, font=("Helvetica", 24), command=self.switch_to_add
        ).pack(side="right", padx=20)
        
        ctk.CTkFrame(self, height=1, fg_color=BORDER_COLOR).pack(fill="x")
        
        month_selector = ctk.CTkFrame(self, fg_color="transparent", height=80)
        month_selector.pack(fill="x", pady=20)
        
        ctk.CTkLabel(month_selector, text="<", font=("Helvetica", 18), text_color=TEXT_SECONDARY).pack(side="left", expand=True, anchor="e", padx=20)
        
        prev_lbl = month_selector.winfo_children()[0]
        prev_lbl.configure(cursor="hand2")
        prev_lbl.bind("<Button-1>", lambda e: self.change_month(-1))
        
        self.month_year_lbl = ctk.CTkLabel(month_selector, text="", font=("Helvetica", 20, "bold"))
        self.month_year_lbl.pack(side="left", expand=True)
        
        ctk.CTkLabel(month_selector, text=">", font=("Helvetica", 18), text_color=TEXT_SECONDARY).pack(side="left", expand=True, anchor="w", padx=20)
        next_lbl = month_selector.winfo_children()[2]
        next_lbl.configure(cursor="hand2")
        next_lbl.bind("<Button-1>", lambda e: self.change_month(1))
        
        self.build_calendar()

    def change_month(self, delta):
        self.current_month += delta
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        elif self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.build_calendar()

    def build_calendar(self):
        if self.calendar_container:
            self.calendar_container.destroy()
            
        month_name = calendar.month_name[self.current_month].upper()
        spaced_month = " ".join(month_name)
        self.month_year_lbl.configure(text=f"{spaced_month}   {self.current_year}")
            
        self.calendar_container = ctk.CTkFrame(self, fg_color=BORDER_COLOR, corner_radius=0)
        self.calendar_container.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        for i, day in enumerate(days):
            self.calendar_container.columnconfigure(i, weight=1, uniform="col")
            header_cell = ctk.CTkFrame(self.calendar_container, fg_color=BG_COLOR, corner_radius=0, height=40)
            header_cell.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
            header_cell.pack_propagate(False)
            ctk.CTkLabel(header_cell, text=day, font=("Helvetica", 12, "bold"), text_color=TEXT_SECONDARY).pack(pady=10)
            
        first_weekday, num_days = calendar.monthrange(self.current_year, self.current_month)
        start_col = first_weekday
        
        day_counter = 1
        for row in range(1, 7):
            self.calendar_container.rowconfigure(row, weight=1, uniform="row")
            for col in range(7):
                cell = ctk.CTkFrame(self.calendar_container, fg_color=BG_COLOR, corner_radius=0)
                cell.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
                
                if (row == 1 and col < start_col) or day_counter > num_days:
                    continue
                
                ctk.CTkLabel(cell, text=str(day_counter), font=("Helvetica", 14), text_color=TEXT_PRIMARY).pack(anchor="nw", padx=10, pady=10)
                
                date_key = f"{self.current_year}-{self.current_month:02d}-{day_counter:02d}"
                if date_key in self.master.events:
                    event_name = self.master.events[date_key]
                    display_name = (event_name[:12] + '..') if len(event_name) > 12 else event_name
                    
                    event_lbl = ctk.CTkLabel(cell, text=f"● {display_name.upper()}", text_color=ACCENT_COLOR, font=("Helvetica", 10, "bold"))
                    event_lbl.pack(side="bottom", anchor="w", padx=10, pady=10)
                    
                    event_lbl.bind("<Button-1>", lambda e, d=date_key: self.switch_to_details(d))
                    cell.bind("<Button-1>", lambda e, d=date_key: self.switch_to_details(d))
                    cell.configure(cursor="hand2")
                    
                day_counter += 1

class AddEventView(ctk.CTkFrame):
    def __init__(self, master, switch_back):
        super().__init__(master, fg_color=BG_COLOR)
        self.switch_back = switch_back
        
        topbar = ctk.CTkFrame(self, height=60, fg_color=BG_COLOR, corner_radius=0)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        ctk.CTkLabel(topbar, text="🗓️ EVENT PLANNER", font=("Helvetica", 14, "bold"), text_color=TEXT_SECONDARY).pack(side="left", padx=20)
        ctk.CTkFrame(self, height=1, fg_color=BORDER_COLOR).pack(fill="x")
        
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(expand=True)
        
        ctk.CTkLabel(content, text="New Event", font=("Helvetica", 32), text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkFrame(content, height=2, width=150, fg_color=ACCENT_COLOR).pack(anchor="w", pady=(5, 40))
        
        ctk.CTkLabel(content, text="EVENT NAME", font=("Helvetica", 10, "bold"), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.name_input = UnderlineEntry(content, placeholder="Untitled Gathering")
        self.name_input.pack(fill="x", pady=(0, 30), ipadx=200)
        
        ctk.CTkLabel(content, text="DATE", font=("Helvetica", 10, "bold"), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.date_input = UnderlineEntry(content, placeholder="Select Date", icon="📅", icon_command=self.open_datepicker, readonly=True)
        self.date_input.pack(fill="x", pady=(0, 40))
        
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=20)
        
        ctk.CTkButton(btn_frame, text="SAVE EVENT", font=("Helvetica", 12, "bold"), fg_color=ACCENT_COLOR, hover_color="#2d2ddb", command=self.save_event).pack(side="right", padx=(10, 0))
        ctk.CTkButton(btn_frame, text="Cancel", font=("Helvetica", 12), fg_color="transparent", text_color=TEXT_PRIMARY, border_width=1, border_color=BORDER_COLOR, hover_color=BG_SECONDARY, command=self.switch_back).pack(side="right")

    def open_datepicker(self):
        current_val = self.date_input.get_text()
        DatePickerPopup(self, self.set_date, initial_date=current_val if current_val else None)

    def set_date(self, date_str):
        self.date_input.set_text(date_str)

    def save_event(self):
        name = self.name_input.get_text()
        date_str = self.date_input.get_text()
        if name and date_str:
            self.master.events[date_str] = name
            self.name_input.set_text("")
            self.date_input.set_text("")
            self.switch_back()

class EventDetailsView(ctk.CTkFrame):
    def __init__(self, master, switch_back):
        super().__init__(master, fg_color=BG_COLOR)
        self.switch_back = switch_back
        self.current_date = None
        self.is_editing = False
        
        self.content = ctk.CTkFrame(self, fg_color="transparent", width=600)
        self.content.pack(expand=True, fill="both", padx=150, pady=100)
        
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(header, text="🗓️ Event Details", font=("Helvetica", 16, "bold"), text_color=TEXT_PRIMARY).pack(side="left")
        
        ctk.CTkButton(header, text="🗑", width=30, fg_color=BG_SECONDARY, hover_color=BORDER_COLOR, text_color=ACCENT_COLOR, font=("Helvetica", 18), command=self.delete_event).pack(side="right")
        
        ctk.CTkFrame(self.content, height=1, fg_color=BORDER_COLOR).pack(fill="x", pady=(0, 30))
        
        self.title_lbl = ctk.CTkLabel(self.content, text="", font=("Helvetica", 42, "bold"), text_color=TEXT_PRIMARY)
        self.title_lbl.pack(anchor="w")
        self.subtitle_lbl = ctk.CTkLabel(self.content, text="", font=("Helvetica", 16), text_color=TEXT_SECONDARY)
        self.subtitle_lbl.pack(anchor="w", pady=(5, 30))
        
        ctk.CTkFrame(self.content, height=1, fg_color=BORDER_COLOR).pack(fill="x", pady=15)
        
        self.row1 = ctk.CTkFrame(self.content, fg_color="transparent")
        self.row1.pack(fill="x", pady=10)
        ctk.CTkLabel(self.row1, text="EVENT NAME", font=("Helvetica", 12), text_color=TEXT_SECONDARY, width=200, anchor="w").pack(side="left")
        
        self.val_name_lbl = ctk.CTkLabel(self.row1, text="", font=("Helvetica", 14), text_color=TEXT_PRIMARY, anchor="w")
        self.val_name_lbl.pack(side="left")
        self.val_name_entry = UnderlineEntry(self.row1, placeholder="Event Name")
        
        ctk.CTkFrame(self.content, height=1, fg_color=BORDER_COLOR).pack(fill="x", pady=15)
        
        self.row2 = ctk.CTkFrame(self.content, fg_color="transparent")
        self.row2.pack(fill="x", pady=10)
        ctk.CTkLabel(self.row2, text="EVENT DATE", font=("Helvetica", 12), text_color=TEXT_SECONDARY, width=200, anchor="w").pack(side="left")
        
        self.val_date_lbl = ctk.CTkLabel(self.row2, text="", font=("Helvetica", 14), text_color=TEXT_PRIMARY, anchor="w")
        self.val_date_lbl.pack(side="left")
        
        self.val_date_entry = UnderlineEntry(self.row2, placeholder="Select Date", icon="📅", icon_command=self.open_datepicker, readonly=True)
        
        btn_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=50)
        
        self.edit_btn = ctk.CTkButton(btn_frame, text="Edit Details", font=("Helvetica", 14, "bold"), fg_color=ACCENT_COLOR, hover_color="#2d2ddb", command=self.toggle_edit)
        self.edit_btn.pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(btn_frame, text="Cancel", font=("Helvetica", 14), fg_color="transparent", text_color=TEXT_PRIMARY, border_width=1, border_color=BORDER_COLOR, hover_color=BG_SECONDARY, command=self.switch_back).pack(side="left")

    def load_event(self, date_str):
        self.current_date = date_str
        name = self.master.events.get(date_str, "")
        
        self.title_lbl.configure(text=name)
        self.subtitle_lbl.configure(text=f"Scheduled for {date_str}")
        
        self.val_name_lbl.configure(text=name)
        self.val_date_lbl.configure(text=date_str)
        
        if self.is_editing:
            self.toggle_edit()

    def open_datepicker(self):
        current_val = self.val_date_entry.get_text()
        DatePickerPopup(self, self.set_date, initial_date=current_val if current_val else None)

    def set_date(self, date_str):
        self.val_date_entry.set_text(date_str)

    def toggle_edit(self):
        self.is_editing = not self.is_editing
        
        if self.is_editing:
            self.edit_btn.configure(text="Save Changes")
            self.val_name_lbl.pack_forget()
            self.val_date_lbl.pack_forget()
            
            self.val_name_entry.set_text(self.val_name_lbl.cget("text"))
            self.val_name_entry.pack(side="left", fill="x", expand=True)
            
            self.val_date_entry.set_text(self.val_date_lbl.cget("text"))
            self.val_date_entry.pack(side="left", fill="x", expand=True)
        else:
            new_name = self.val_name_entry.get_text()
            new_date = self.val_date_entry.get_text()
            
            if self.current_date != new_date:
                del self.master.events[self.current_date]
            
            self.master.events[new_date] = new_name
            self.current_date = new_date
            
            self.edit_btn.configure(text="Edit Details")
            self.val_name_entry.pack_forget()
            self.val_date_entry.pack_forget()
            
            self.load_event(new_date)
            self.val_name_lbl.pack(side="left")
            self.val_date_lbl.pack(side="left")

    def delete_event(self):
        if self.current_date in self.master.events:
            del self.master.events[self.current_date]
        self.switch_back()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Event Planner")
        self.geometry("1000x700")
        self.configure(fg_color=BG_COLOR)
        
        today = datetime.now()
        test_date = f"{today.year}-{today.month:02d}-15"
        self.events = {
            test_date: "PAP0124"
        }
        
        self.month_view = MonthView(self, self.show_add_event, self.show_event_details)
        self.add_event_view = AddEventView(self, self.show_month_view)
        self.event_details_view = EventDetailsView(self, self.show_month_view)
        
        self.show_month_view()

    def hide_all(self):
        self.month_view.pack_forget()
        self.add_event_view.pack_forget()
        self.event_details_view.pack_forget()

    def show_month_view(self):
        self.hide_all()
        self.month_view.build_calendar()
        self.month_view.pack(fill="both", expand=True)
        self.update_idletasks()

    def show_add_event(self):
        self.hide_all()
        self.add_event_view.pack(fill="both", expand=True)
        self.update_idletasks()

    def show_event_details(self, date_str):
        self.hide_all()
        self.event_details_view.load_event(date_str)
        self.event_details_view.pack(fill="both", expand=True)
        self.update_idletasks()

if __name__ == "__main__":
    app = App()
    app.mainloop()