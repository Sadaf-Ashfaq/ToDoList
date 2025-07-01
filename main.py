from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from ttkthemes import ThemedTk
from task_manager import addTask, toggleTaskStatus, deleteTask, sort_by_status
import task_data  # ✅ Correct import

# ---------- Initialize Themed Window ----------
root = ThemedTk(theme="radiance")
root.title("To-Do List with Calendar")
root.geometry("500x550")
root.resizable(False, False)

# ---------- Load Images ----------
def load_image(path, size):
    img = Image.open(path)
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

bg_image = load_image("Image/look.jpeg", (500, 550))
add_img = load_image("Image/add.png", (32, 32))
delete_img = load_image("Image/delete.png", (32, 32))
mark_img = load_image("Image/mark.png", (32, 32))
all_img = load_image("Image/all.png", (32, 32))
completed_img = load_image("Image/completed.png", (32, 32))
incompleted_img = load_image("Image/incompleted.png", (32, 32))
Image_icon = load_image("Image/task.png", (32, 32))
root.iconphoto(False, Image_icon)

# ---------- Background ----------
bg_label = Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# ---------- Header ----------
header = Label(root, text="  My To-Do List", compound=LEFT, font=("Arial", 16, "bold"), bg="white", anchor="w", padx=10)
header.pack(fill=X, pady=5)

# ---------- Entry + Calendar Frame ----------
frame = ttk.Frame(root)
frame.pack(pady=10)

# ---------- Entry Placeholder ----------
def set_placeholder(entry, text):
    entry.insert(0, text)
    entry.config(foreground='gray')
    def on_focus_in(event):
        if entry.get() == text:
            entry.delete(0, END)
            entry.config(foreground='black')
    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, text)
            entry.config(foreground='gray')
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

task_entry = ttk.Entry(frame, font=("Arial", 12), width=25)
task_entry.grid(row=0, column=0, padx=5)
set_placeholder(task_entry, "Enter task...")

#date_entry = DateEntry(frame, width=12, background='white', foreground='black')
date_entry = DateEntry(
    frame, 
    width=12, 
    background='white',
    foreground='black',
    bordercolor='gray',
    headersbackground='white',
    headersforeground='black',
    selectbackground="#B6184F",
    normalbackground='white',
    weekendbackground='white',
    weekendforeground='black',
    othermonthbackground='#f0f0f0',
    othermonthforeground='gray',
    arrowcolor='black',
    borderwidth=1
)
date_entry.grid(row=0, column=1, padx=5)

# ---------- Listbox ----------
listbox = Listbox(
    root,
    font=("Arial", 12),
    width=50,
    height=12,
    bg="white",
    fg="#8E0937",
    bd=0,
    highlightthickness=1,
    relief=FLAT
)
listbox.pack(pady=10)

# ---------- Refresh Function ----------
def refresh_task_display():
    listbox.delete(0, END)
    for task in task_data.master_task_list:
        due_date = task['due_date'].strftime("%Y-%m-%d") if hasattr(task['due_date'], 'strftime') else task['due_date']
        status = "[✓]" if task["completed"] else "[✗]"
        listbox.insert(END, f"{task['text']} - Due: {due_date} {status}")

# Initial display of tasks
task_data.load_tasks()
refresh_task_display()

# ---------- Button Hover Effect ----------
def on_enter(e):
    e.widget.config(bg="#f0f0f0")
def on_leave(e):
    e.widget.config(bg="white")

# ---------- Button Frame ----------
btn_frame = ttk.Frame(root)
btn_frame.pack(pady=10, ipadx=10)

buttons = [
    (add_img, lambda: [addTask(task_entry, date_entry, listbox), refresh_task_display()]),
    (delete_img, lambda: [deleteTask(listbox), refresh_task_display()]),
    (mark_img, lambda: [toggleTaskStatus(listbox), refresh_task_display()]),
    (all_img, lambda: sort_by_status(listbox, "all")),
    (completed_img, lambda: sort_by_status(listbox, "completed")),
    (incompleted_img, lambda: sort_by_status(listbox, "incomplete"))
]

for img, cmd in buttons:
    btn = Button(btn_frame, image=img, command=cmd, bg="white", bd=0)
    btn.pack(side=LEFT, padx=8, pady=5)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# ---------- Keep image references ----------
root.bg_image = bg_image

# ---------- Start App ----------
root.mainloop()
