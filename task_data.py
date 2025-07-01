import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"
master_task_list = []

def load_tasks():
    global master_task_list
    try:
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as f:
                tasks = json.load(f)
                master_task_list = []
                
                for task in tasks:
                    # Ensure all required fields exist
                    if not all(key in task for key in ['text', 'due_date', 'completed']):
                        continue
                    
                    # Convert string date back to date object if needed
                    if isinstance(task['due_date'], str):
                        try:
                            task['due_date'] = datetime.strptime(task['due_date'], "%Y-%m-%d").date()
                        except ValueError:
                            # If date is invalid, use today's date
                            task['due_date'] = datetime.now().date()
                    
                    master_task_list.append(task)
                
                print(f"Loaded {len(master_task_list)} tasks from storage")  # Debug
        else:
            master_task_list = []
            print("No existing tasks file found")  # Debug
    except Exception as e:
        print(f"Error loading tasks: {str(e)}")
        master_task_list = []

def save_tasks(tasks):
    try:
        tasks_to_save = []
        for task in tasks:
            task_copy = task.copy()
            # Convert date to string if it's a date object
            if hasattr(task_copy['due_date'], 'strftime'):
                task_copy['due_date'] = task_copy['due_date'].strftime("%Y-%m-%d")
            tasks_to_save.append(task_copy)
        
        with open(TASKS_FILE, "w") as f:
            json.dump(tasks_to_save, f, indent=4)
        print(f"Saved {len(tasks_to_save)} tasks")  # Debug
    except Exception as e:
        print(f"Error saving tasks: {str(e)}")