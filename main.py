import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from database import add_task, delete_task, get_all_tasks, update_task

# primary window settings
root = tk.Tk()
root.title("PriorityManager")

title = ttk.Label(root, text="PriorityManager", font=("Arial", 24))
title.pack(padx=20,pady=20)

# course label and input 
course_label = ttk.Label(root, text="Course Name:")
course_label.pack(padx=5, pady=2)

course_entry = tk.StringVar()
course = ttk.Entry(root, textvariable=course_entry, width=30)
course.pack(padx=10, pady=2)

# assignment label and input
assignment_label = ttk.Label(root, text="Assignment:")
assignment_label.pack(padx=10, pady=2)

assignment_entry = tk.StringVar()
assignment = ttk.Entry(root, textvariable=assignment_entry, width=30)
assignment.pack(padx=10, pady=2)

# date picker
cal_label = ttk.Label(root, text='Due Date:')
cal_label.pack(padx=10, pady=2)
cal = Calendar(root)
cal.pack(padx=10, pady=2)

# priority picker
priority_label = ttk.Label(root, text="Priority:")
priority_label.pack(padx=10, pady=2)

priority_dropdown = ttk.Combobox(root, values=['Low','Medium','High'], state="readonly")
priority_dropdown.pack(padx=10, pady=2)

# treeview
table = ttk.Treeview(root, columns=("Course", "Assignment", "Due Date", "Priority", "Status"), show = "headings")

table.heading("Course", text="Course")
table.column("Course", width=150)

table.heading("Assignment", text="Assignment")
table.column("Assignment", width=150)

table.heading("Due Date", text="Due Date")
table.column("Due Date", width=150)

table.heading("Priority", text="Priority")
table.column("Priority", width=150)

table.heading("Status", text="Status")
table.column("Status", width=150)

table.pack(padx=10, pady=10, fill="both")

# add button
def on_add_click(event):
    course_input = course.get()
    assignment_input = assignment.get()
    date_input = cal.get_date()
    priority_input = priority_dropdown.get()
    status = 'pending'

    if not course_input or not assignment_input or not date_input or not priority_input:
        messagebox.showwarning("Missing information", "ERROR: Inputs are not filled out completely!")

    task_id = add_task(course_input, assignment_input, date_input, priority_input, status)
    table.insert("", "end", iid=str(task_id), values=(course_input, assignment_input, date_input, priority_input, status))
    print(f"You entered: {course_input}, {assignment_input}, {date_input}, {priority_input}, {status}")

    course_entry.set("")
    assignment_entry.set("")
    priority_dropdown.set("")

add_button = ttk.Button(root, text="Add")
add_button.place(x=50, y=20)
add_button.pack(padx=10, pady=5)
add_button.bind('<Button-1>', on_add_click)

# remove button
def on_remove_click(event):
    return 0

remove_button = ttk.Button(root, text="Remove")
remove_button.pack(padx=10, pady=5)

# status button
def on_status_click(event):
    return 0

status_button = ttk.Button(root, text="Mark as done")
status_button.pack(padx=10, pady=5)

def refresh_table():
    for task in get_all_tasks():
        table.insert()

root.mainloop()