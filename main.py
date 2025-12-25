from tkinter import *
from logic import tool
import ctypes
win = Tk()
# 1. SET THE ICON (Must be a .ico file in the same folder)
try:
    win.iconbitmap("app_icon.ico")
except Exception as e:
    print(f"Icon not found, using default: {e}")

# 2. THE TASKBAR
# This tells Windows: "This is a real app, not just a generic Python script."
try:
    myappid = 'my.progress.tracker.v1' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass # Non-windows systems won't crash
win.geometry("620x250")    #DECIDES WIDTH AND HEIGHT OF DISPLAY BOX
win.configure(bg="#222222")

# FRAMES ARE EQUIVALENT TO DIVS IN THIS
# 🔹 REMOVE SYSTEM BORDER (needed for custom border)
win.overrideredirect(True)

# ===== CUSTOM BORDER =====
border = Frame(win, bg="#000000")
border.pack(fill=BOTH, expand=True,padx=1,pady=1)

# ===== MAIN CONTENT AREA =====
main_frame = Frame(border, bg="#222222")
main_frame.pack(fill=BOTH, expand=True)

# ===== TITLE BAR =====
title_bar = Frame(main_frame, bg="#000000")
title_bar.pack(fill=X)

title_label = Label(
    title_bar,
    text="Progress Tracker",
    bg="#000000",
    fg="#EAEAEA",
    font=("Segoe UI", 10, "bold")
)
title_label.pack(side=LEFT, padx=10)

close_btn = Button(
    title_bar,
    text=" ✕ ",
    bg="#000000",
    fg="#FFFFFF",
    relief=FLAT,
    command=win.destroy,
    font=("Segoe UI", 10, "bold")
)

def change(event):
    close_btn.configure(bg="#FF0000")

def back(event):
    close_btn.configure(bg="#000000")

close_btn.bind("<Enter>", change)
close_btn.bind("<Leave>", back)
close_btn.pack(side=RIGHT, padx=0)


# ===== WINDOW DRAG FUNCTION =====
def start_move(event):
    win.x = event.x
    win.y = event.y

def stop_move(event):
    win.x = None
    win.y = None

def do_move(event):
    x = win.winfo_x() + (event.x - win.x)
    y = win.winfo_y() + (event.y - win.y)
    win.geometry(f"+{x}+{y}")

title_bar.bind("<Button-1>", start_move)
title_bar.bind("<ButtonRelease-1>", stop_move)
title_bar.bind("<B1-Motion>", do_move)

title_label.bind("<Button-1>", start_move)
title_label.bind("<ButtonRelease-1>", stop_move)
title_label.bind("<B1-Motion>", do_move)

# ===== OPACITY SETTINGS =====
ACTIVE_OPACITY = 1.0
INACTIVE_OPACITY = 0.2

def on_focus_in(event):
    win.attributes("-alpha", ACTIVE_OPACITY)

def on_focus_out(event):
    win.attributes("-alpha", INACTIVE_OPACITY)

win.bind("<FocusIn>", on_focus_in)
win.bind("<FocusOut>", on_focus_out)

# ===== PLACEHOLDER FUNCTION  =====
def add_placeholder(entry, text):
    entry.insert(0, text)
    entry.config(fg="grey")

    def on_focus_in(event):
        if entry.get() == text:
            entry.delete(0, END)
            entry.config(fg="black")

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, text)
            entry.config(fg="grey")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# class for outputs and inputs
class modify:
    def __init__(self):
        self.tool = tool()
        self.tool.create_tree()
    
    def update(self):
        date_val = date_entry.get()
        if date_val == "dd-mm-yyyy":
            stat.config(text="STATUS : Please enter date", fg="#ff4040")
            win.config(bg="#ff0000")
            return
        try:
            self.tool.to_tuple(date_val) 
        except:
            stat.config(text="STATUS : Invalid format (use dd-mm-yyyy)", fg="#ff0000")
            win.config(bg="#ff0000")
            return
        tasks = number.get()
        if tasks <= 0:
            stat.config(text=f"STATUS : enter valid number of tasks", fg="#ff0000")
            win.config(bg="#ff0000")
            return
        response = self.tool.update(date_val, tasks)

        if response is True:
            stat.config(text=f"STATUS : Updated {date_val} Successfully...", fg="#40ff80")
            win.config(bg="#40ff00")
            self.clear_update_inputs()
        else:
            stat.config(text="STATUS : you gave invalid data", fg="#ff0000")
            win.config(bg="#ff0000")
    
    def clear_update_inputs(self):
        date_entry.delete(0, END)
        add_placeholder(date_entry, "dd-mm-yyyy")
        number_entry.delete(0, END)
        number.set(0)

    def clear_query_inputs(self):
        """Resets query fields back to placeholders"""
        date_entry_q.delete(0, END)
        add_placeholder(date_entry_q, "dd-mm-yyyy")
        date_entry_q1.delete(0, END)
        add_placeholder(date_entry_q1, "dd-mm-yyyy")

    def query(self):
        st_date = start_date.get()
        en_date = end_date.get()
        if st_date == "dd-mm-yyyy" or en_date == "dd-mm-yyyy":
            stat.config(text="STATUS : Please enter both dates", fg="#ff4040")
            win.config(bg="#ff0000")
            return
        
        # --- NEW RANGE CHECK ---
        try:
            if self.tool.to_tuple(st_date) > self.tool.to_tuple(en_date):
                stat.config(text="STATUS : Start date must be before End date", fg="#ff4040")
                win.config(bg="#ff0000")
                return
        except:
            stat.config(text="STATUS : Invalid date format", fg="#ff0000")
            win.config(bg="#ff0000")
            return

        response = self.tool.query(st_date, en_date)
        if response == -1:
            stat.config(text="STATUS : you gave invalid data", fg="#ff0000")
            win.config(bg="#ff0000")
        else:
            stat.config(text=f"tasks performed between {st_date} and {en_date} = {response}", fg="#00aaff")
            win.config(bg="#00aaff")
            self.clear_query_inputs() # --- NEW RESETTER CALL ---
engine = modify()        
# status and output bar, this will show errors for wrong query and output for correct query and success message after successful update
output = Frame(main_frame, bg="#1a1a1a")
output.pack(side=BOTTOM,pady=(0,5), padx=6,fill=X)

stat = Label(
    output,
    text="STATUS :",
    fg="white",
    bg="#1A1A1A",
    font=("Segoe UI", 10, "bold")
)
stat.pack(side=LEFT, padx=(5,5), pady=(5,5))

# main:to display output we will, just change the text of stat label
# ===== LEFT FRAME =====
leftframe = Frame(main_frame, bg="#1A1A1A")
leftframe.pack(side=LEFT, ipadx=15, ipady=15, padx=5, pady=5)

head = Label(
    leftframe,
    text="UPDATE DETAILS",
    fg="white",
    bg="#1A1A1A",
    font=("Segoe UI", 10, "bold")
)
head.pack(side=TOP, pady=3)

date = StringVar()

date_row = Frame(leftframe, bg="#1A1A1A")
date_row.pack(side=TOP, pady=10)

date_label = Label(
    date_row,
    text="Enter Date:",
    fg="white",
    bg="#1A1A1A",
    font=("Segoe UI", 10)
)
date_label.pack(side=LEFT, padx=(0, 93))

date_entry = Entry(date_row, textvariable=date, bd=0, relief="flat", highlightthickness=0)
date_entry.pack(side=LEFT)

add_placeholder(date_entry, "dd-mm-yyyy")   # ← added

number_row = Frame(leftframe, bg="#1A1A1A")
number_row.pack(side=TOP, pady=6)

number_label = Label(
    number_row,
    text="how many tasks you did: ",
    fg="white",
    bg="#1A1A1A",
    font=("Segoe UI", 10)
)
number = IntVar()
number_label.pack(side=LEFT, padx=(0, 10))

number_entry = Entry(number_row, textvariable=number, bd=0, relief="flat", highlightthickness=0)
number_entry.pack(side=LEFT)









update_btn = Button(
    leftframe,
    text=" Update ",
    bg="#4080fF",
    fg="#FFFFFF",
    relief=FLAT,
    command=engine.update,
    font=("Segoe UI", 10, "bold")
)

def change2(event):
    update_btn.configure(bg="#0055FF")

def back2(event):
    update_btn.configure(bg="#4080ff")

update_btn.bind("<Enter>", change2)
update_btn.bind("<Leave>", back2)
update_btn.pack(side=BOTTOM, pady=15, ipadx=20)

# ===== RIGHT FRAME =====
rightframe = Frame(main_frame, bg="#1A1A1A")
rightframe.pack(side=RIGHT, ipadx=15, ipady=15, padx=(0, 5), pady=5)

head2 = Label(
    rightframe,
    text="GET PROGRESS DETAILS",
    fg="white",
    bg="#1A1A1A",
    font=("Segoe UI", 10, "bold")
)
head2.pack(side=TOP, pady=3)

start_date = StringVar()

date_row_q = Frame(rightframe, bg="#1A1A1A")
date_row_q.pack(side=TOP, pady=10)

date_label_start = Label(
    date_row_q,
    text="Enter Start Date:",
    fg="white",
    bg="#1A1A1A",
    font=("Segoe UI", 10)
)
date_label_start.pack(side=LEFT, padx=(0, 43))

date_entry_q = Entry(date_row_q, textvariable=start_date, bd=0, relief="flat", highlightthickness=0)
date_entry_q.pack(side=LEFT)

add_placeholder(date_entry_q, "dd-mm-yyyy")   # ← added

end_date = StringVar()

date_row_q1 = Frame(rightframe, bg="#1A1A1A")
date_row_q1.pack(side=TOP, pady=8)

date_label_end = Label(
    date_row_q1,
    text="Enter End Date:",
    fg="white",
    bg="#1A1A1A",
    font=("Segoe UI", 10)
)
date_label_end.pack(side=LEFT, padx=(0, 49))

date_entry_q1 = Entry(date_row_q1, textvariable=end_date, bd=0, relief="flat", highlightthickness=0)
date_entry_q1.pack(side=LEFT)

add_placeholder(date_entry_q1, "dd-mm-yyyy")   # ← added

query_btn = Button(
    rightframe,
    text=" Get ",
    bg="#4080fF",
    fg="#FFFFFF",
    relief=FLAT,
    command=engine.query,
    font=("Segoe UI", 10, "bold")
)

def change3(event):
    query_btn.configure(bg="#0055FF")

def back3(event):
    query_btn.configure(bg="#4080ff")

query_btn.bind("<Enter>", change3)
query_btn.bind("<Leave>", back3)
query_btn.pack(side=BOTTOM, pady=15, ipadx=20)






win.mainloop()
