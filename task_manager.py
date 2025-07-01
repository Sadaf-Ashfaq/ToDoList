from tkinter import messagebox, END
from datetime import datetime
import task_data  # ✅ Correct import

def addTask(task_entry, date_entry, listbox):
    task_text = task_entry.get().strip()
    due_date = date_entry.get_date()

    if not task_text or task_text == "Enter task...":
        messagebox.showwarning("Warning", "You must enter a valid task.")
        return

    task = {
        "text": task_text,
        "due_date": due_date,
        "completed": False
    }
    task_data.master_task_list.append(task)
    task_data.save_tasks(task_data.master_task_list)
    refresh_listbox(listbox)

def refresh_listbox(listbox):
    listbox.delete(0, END)
    for task in task_data.master_task_list:
        status = "[✓]" if task["completed"] else "[✗]"
        due_date = task["due_date"].strftime("%Y-%m-%d") if hasattr(task["due_date"], 'strftime') else task["due_date"]
        listbox.insert(END, f"{task['text']} - Due: {due_date} {status}")

def toggleTaskStatus(listbox):
    selected = listbox.curselection()
    if not selected:
        return

    index = selected[0]
    task = task_data.master_task_list[index]
    task['completed'] = not task['completed']
    task_data.save_tasks(task_data.master_task_list)
    refresh_listbox(listbox)

def deleteTask(listbox):
    selected = listbox.curselection()
    if not selected:
        return
    index = selected[0]
    task_data.master_task_list.pop(index)
    task_data.save_tasks(task_data.master_task_list)
    refresh_listbox(listbox)

def sort_by_status(listbox, filter_type):
    listbox.delete(0, END)
    for task in task_data.master_task_list:
        show_task = (
            (filter_type == "all") or
            (filter_type == "completed" and task["completed"]) or
            (filter_type == "incomplete" and not task["completed"])
        )
        if show_task:
            due_date = task['due_date'].strftime("%Y-%m-%d") if hasattr(task['due_date'], 'strftime') else task['due_date']
            status = "[✓]" if task["completed"] else "[✗]"
            listbox.insert(END, f"{task['text']} - Due: {due_date} {status}")
