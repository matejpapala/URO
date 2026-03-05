import customtkinter as ctk

BG_COLOR = "#1c1c1c"
BG_SECONDARY = "#404040"
ACCENT_COLOR = "#3c3cf6"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#94a3b8"
BORDER_COLOR = "#404040"

ctk.set_appearance_mode("dark")

class UnderlineEntry(ctk.CTkFrame):
    def __init__(self, master, placeholder, icon=None, **kwargs):
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
        
        if icon:
            self.icon_label = ctk.CTkLabel(self, text=icon, text_color=TEXT_SECONDARY, font=("Helvetica", 16))
            self.icon_label.grid(row=0, column=1, sticky="e", padx=(0, 5))
            
        self.line = ctk.CTkFrame(self, height=1, fg_color=BORDER_COLOR)
        self.line.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(2, 0))

class MonthView(ctk.CTkFrame):
    def __init__(self, master, switch_to_add, switch_to_details):
        super().__init__(master, fg_color=BG_COLOR)
        self.switch_to_add = switch_to_add
        self.switch_to_details = switch_to_details
        
        topbar = ctk.CTkFrame(self, height=60, fg_color=BG_COLOR, corner_radius=0)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        
        ctk.CTkLabel(topbar, text="🗓️ EVENT PLANNER", font=("Helvetica", 14, "bold"), text_color=TEXT_SECONDARY).pack(side="left", padx=20)
        
        add_btn = ctk.CTkButton(
            topbar, text="+", width=40, fg_color="transparent", hover_color=BG_SECONDARY,
            text_color=TEXT_PRIMARY, font=("Helvetica", 24), command=self.switch_to_add
        )
        add_btn.pack(side="right", padx=20)
        
        ctk.CTkFrame(self, height=1, fg_color=BORDER_COLOR).pack(fill="x")
        
        month_selector = ctk.CTkFrame(self, fg_color="transparent", height=80)
        month_selector.pack(fill="x", pady=20)
        
        ctk.CTkLabel(month_selector, text="<", font=("Helvetica", 18), text_color=TEXT_SECONDARY).pack(side="left", expand=True, anchor="e", padx=20)
        ctk.CTkLabel(month_selector, text="J U L Y", font=("Helvetica", 20, "bold")).pack(side="left", expand=True)
        ctk.CTkLabel(month_selector, text=">", font=("Helvetica", 18), text_color=TEXT_SECONDARY).pack(side="left", expand=True, anchor="w", padx=20)
        
        calendar_container = ctk.CTkFrame(self, fg_color=BORDER_COLOR, corner_radius=0)
        calendar_container.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
        for i, day in enumerate(days):
            calendar_container.columnconfigure(i, weight=1)
            header_cell = ctk.CTkFrame(calendar_container, fg_color=BG_COLOR, corner_radius=0, height=40)
            header_cell.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
            header_cell.pack_propagate(False)
            ctk.CTkLabel(header_cell, text=day, font=("Helvetica", 12, "bold"), text_color=TEXT_SECONDARY).pack(pady=10)
            
        for row in range(1, 6):
            calendar_container.rowconfigure(row, weight=1)
            for col in range(7):
                day_num = (row - 1) * 7 + col - 2
                
                cell = ctk.CTkFrame(calendar_container, fg_color=BG_COLOR, corner_radius=0)
                cell.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
                
                if 1 <= day_num <= 31:
                    ctk.CTkLabel(cell, text=str(day_num), font=("Helvetica", 14), text_color=TEXT_PRIMARY).pack(anchor="nw", padx=10, pady=10)
                    
                    if day_num == 15:
                        event_lbl = ctk.CTkLabel(cell, text="● EVENT", text_color=ACCENT_COLOR, font=("Helvetica", 10, "bold"))
                        event_lbl.pack(side="bottom", anchor="w", padx=10, pady=10)
                        event_lbl.bind("<Button-1>", lambda e: self.switch_to_details())
                        cell.bind("<Button-1>", lambda e: self.switch_to_details())
                        cell.configure(cursor="hand2")

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
        
        title = ctk.CTkLabel(content, text="New Event", font=("Helvetica", 32), text_color=TEXT_PRIMARY)
        title.pack(anchor="w")
        ctk.CTkFrame(content, height=2, width=150, fg_color=ACCENT_COLOR).pack(anchor="w", pady=(5, 40))
        
        ctk.CTkLabel(content, text="EVENT NAME", font=("Helvetica", 10, "bold"), text_color=TEXT_SECONDARY).pack(anchor="w")
        UnderlineEntry(content, placeholder="Untitled Gathering").pack(fill="x", pady=(0, 30), ipadx=200)
        
        ctk.CTkLabel(content, text="DATE", font=("Helvetica", 10, "bold"), text_color=TEXT_SECONDARY).pack(anchor="w")
        UnderlineEntry(content, placeholder="YYYY - MM - DD", icon="📅").pack(fill="x", pady=(0, 40))
        
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=20)
        
        save_btn = ctk.CTkButton(btn_frame, text="SAVE EVENT", font=("Helvetica", 12, "bold"), fg_color=ACCENT_COLOR, hover_color="#2d2ddb")
        save_btn.pack(side="right", padx=(10, 0))
        
        cancel_btn = ctk.CTkButton(
            btn_frame, text="Cancel", font=("Helvetica", 12), fg_color="transparent", text_color=TEXT_PRIMARY,
            border_width=1, border_color=BORDER_COLOR, hover_color=BG_SECONDARY, command=self.switch_back
        )
        cancel_btn.pack(side="right")

class EventDetailsView(ctk.CTkFrame):
    def __init__(self, master, switch_back):
        super().__init__(master, fg_color=BG_COLOR)
        self.switch_back = switch_back
        
        content = ctk.CTkFrame(self, fg_color="transparent", width=600)
        content.pack(expand=True, fill="both", padx=150, pady=100)
        
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(header, text="🗓️ Event Details", font=("Helvetica", 16, "bold"), text_color=TEXT_PRIMARY).pack(side="left")
        
        del_btn = ctk.CTkButton(
            header, text="🗑", width=30, fg_color=BG_SECONDARY, hover_color=BORDER_COLOR,
            text_color=ACCENT_COLOR, font=("Helvetica", 18), command=self.switch_back
        )
        del_btn.pack(side="right")
        
        ctk.CTkFrame(content, height=1, fg_color=BORDER_COLOR).pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(content, text="Team Meeting", font=("Helvetica", 42, "bold"), text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(content, text="Scheduled for July 15", font=("Helvetica", 16), text_color=TEXT_SECONDARY).pack(anchor="w", pady=(5, 30))
        
        ctk.CTkFrame(content, height=1, fg_color=BORDER_COLOR).pack(fill="x", pady=15)
        
        row1 = ctk.CTkFrame(content, fg_color="transparent")
        row1.pack(fill="x", pady=10)
        ctk.CTkLabel(row1, text="EVENT NAME", font=("Helvetica", 12), text_color=TEXT_SECONDARY, width=200, anchor="w").pack(side="left")
        ctk.CTkLabel(row1, text="Team Meeting", font=("Helvetica", 14), text_color=TEXT_PRIMARY, anchor="w").pack(side="left")
        
        ctk.CTkFrame(content, height=1, fg_color=BORDER_COLOR).pack(fill="x", pady=15)
        
        row2 = ctk.CTkFrame(content, fg_color="transparent")
        row2.pack(fill="x", pady=10)
        ctk.CTkLabel(row2, text="EVENT DATE", font=("Helvetica", 12), text_color=TEXT_SECONDARY, width=200, anchor="w").pack(side="left")
        ctk.CTkLabel(row2, text="July 15, 2024", font=("Helvetica", 14), text_color=TEXT_PRIMARY, anchor="w").pack(side="left")
        
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=50)
        
        edit_btn = ctk.CTkButton(btn_frame, text="Edit Details", font=("Helvetica", 14, "bold"), fg_color=ACCENT_COLOR, hover_color="#2d2ddb")
        edit_btn.pack(side="left", padx=(0, 10))
        
        cancel_btn = ctk.CTkButton(
            btn_frame, text="Cancel", font=("Helvetica", 14), fg_color="transparent", text_color=TEXT_PRIMARY,
            border_width=1, border_color=BORDER_COLOR, hover_color=BG_SECONDARY, command=self.switch_back
        )
        cancel_btn.pack(side="left")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Event Planner")
        self.geometry("1000x700")
        self.configure(fg_color=BG_COLOR)
        
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
        self.month_view.pack(fill="both", expand=True)

    def show_add_event(self):
        self.hide_all()
        self.add_event_view.pack(fill="both", expand=True)

    def show_event_details(self):
        self.hide_all()
        self.event_details_view.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()