import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import datetime as dt
from datetime import datetime
from tkcalendar import *
from database import *

# primary window settings
root = tk.Tk()
root.title("Priority Manager")
root.geometry("600x400+550+150") 

title = ttk.Label(root, text="Priority Manager", font=("Arial", 24))
title.pack(padx=20,pady=20)

# new task window
def new_task_window():
    window = Toplevel(root)
    window.title("New Task")
    window.geometry("250x500")

    label = ttk.Label(window, text="New Task", font=("Arial", 24))
    label.pack(pady=20)

    # course label and input 
    course_label = ttk.Label(window, text="Course Name:")
    course_label.pack(padx=5, pady=2)

    course_entry = tk.StringVar()
    course = ttk.Entry(window, textvariable=course_entry, width=30)
    course.pack(padx=10, pady=2)

    # assignment label and input
    assignment_label = ttk.Label(window, text="Assignment:")
    assignment_label.pack(padx=10, pady=2)

    assignment_entry = tk.StringVar()
    assignment = ttk.Entry(window, textvariable=assignment_entry, width=30)
    assignment.pack(padx=10, pady=2)

    # date picker
    cal_label = ttk.Label(window, text='Due Date:')
    cal_label.pack(padx=10, pady=2)
    cal = Calendar(window)
    cal.pack(padx=10, pady=2)

    # priority picker
    priority_label = ttk.Label(window, text="Priority:")
    priority_label.pack(padx=10, pady=2)

    priority_dropdown = ttk.Combobox(window, values=['Low','Medium','High'], state="readonly")
    priority_dropdown.pack(padx=10, pady=2)

    # add button
    def on_add_click():
        course_input = course.get()
        assignment_input = assignment.get()
        date_input = cal.get_date()
        priority_input = priority_dropdown.get()
        status = 'pending'

        if not course_input or not assignment_input or not date_input or not priority_input:
            messagebox.showwarning("Missing information", "ERROR: Inputs are not filled out completely!")
            return
        
        table.tag_configure("Low", background="#00FF08")      
        table.tag_configure("Medium", background="#FFE600")   
        table.tag_configure("High", background="#FF0019")      

        task = add_task(course_input, assignment_input, date_input, priority_input, status)
        table.insert("", "end", iid=str(task), values=(course_input, assignment_input, date_input, priority_input, status), tags=(priority_input,))
        print(f"You entered: {course_input}, {assignment_input}, {date_input}, {priority_input}, {status}")

        messagebox.showinfo("Success", "Task added successfully!")

        course_entry.set("")
        assignment_entry.set("")
        priority_dropdown.set("")

        refresh_table()

        window.destroy()

    add_button = ttk.Button(window, text="Add", command=on_add_click)
    add_button.pack(padx=10, pady=5)

# new task button 
new_button = ttk.Button(root, text="New Task", command=new_task_window)
new_button.place(x=170, y=90, anchor="center")

# edit task window
def on_edit_click():
    row = table.focus()
    selection = table.item(row, 'values')

    if not selection:
        messagebox.showerror("Error", "Please select a task!")
        return

    course = selection[0]
    assignment = selection[1]
    date = selection[2]
    priority = selection[3]
    
    edit_task_window(crs=course, asgmnt=assignment, dte=date, pri=priority)

def edit_task_window(crs, asgmnt, dte, pri):
    window = Toplevel(root)
    window.title("Edit Task")
    window.geometry("250x550")

    label = ttk.Label(window, text="Edit Task", font=("Arial", 24))
    label.pack(pady=20)

    # course label and input 
    course_label = ttk.Label(window, text="Course Name:")
    course_label.pack(padx=5, pady=2)
    
    course_widget = ttk.Entry(window, width=30)
    course_widget.insert(0, crs)
    course_widget.pack(padx=10, pady=2)

    # assignment label and input
    assignment_label = ttk.Label(window, text="Assignment:")
    assignment_label.pack(padx=10, pady=2)

    assignment_widget = ttk.Entry(window, width=30)
    assignment_widget.insert(0, asgmnt)
    assignment_widget.pack(padx=10, pady=2)

    # date picker
    cal_label = ttk.Label(window, text='Due Date:')
    cal_label.pack(padx=10, pady=2)

    date = datetime.strptime(dte, "%m/%d/%y").date()

    cal = Calendar(window, selectmode="day", year=date.year, month=date.month, day=date.day)
    cal.pack(padx=10, pady=2)

    # priority picker
    priority_label = ttk.Label(window, text="Priority:")
    priority_label.pack(padx=10, pady=2)

    priority_dropdown = ttk.Combobox(window, values=['Low','Medium','High'], state="readonly", textvariable=pri)
    priority_dropdown.set(pri)

    priority_dropdown.pack(padx=10, pady=2)

    # update button
    def on_update_click():
        course_input = course_widget.get()
        assignment_input = assignment_widget.get()
        date_input = cal.get_date()
        priority_input = priority_dropdown.get()
        status = 'pending'
        
        row = table.focus()
        selection = table.item(row, 'values')

        start = row.find("id=") + 3
        end = row.find(",", start)
        task_id = int(row[start:end])

        delete_task(task_id)
        table.delete(row)

        task = add_task(course_input, assignment_input, date_input, priority_input, status)
        table.insert("", "end", iid=str(task), values=(course_input, assignment_input, date_input, priority_input, status))
        print(f"You entered: {course_input}, {assignment_input}, {date_input}, {priority_input}, {status}")

        messagebox.showinfo("Success", "Task updated successfully!")

        refresh_table()

        window.destroy()

    update_button = ttk.Button(window, text="Update", command=on_update_click)
    update_button.pack(padx=10, pady=5)

# edit task button
edit_button = ttk.Button(root, text="Edit Task", command=on_edit_click)
edit_button.place(x=290, y=90, anchor="center")

# remove button
def on_remove_click():
    row = table.focus()
    selection = table.item(row, 'values')

    if not selection:
        messagebox.showerror("Error", "Please select a task!")
        return

    start = row.find("id=") + 3
    end = row.find(",", start)
    task_id = int(row[start:end])

    delete_task(task_id)
    table.delete(row)

    messagebox.showinfo("Success", "Task removed successfully!")

# remove task button 
remove_button = ttk.Button(root, text="Remove Task", command=on_remove_click)
remove_button.place(x=420, y=90, anchor="center")

# status button
def on_status_click():
    row = table.focus()
    selection = table.item(row, 'values')

    if not selection:
        messagebox.showerror("Error", "Please select a task!")
        return

    start = row.find("id=") + 3
    end = row.find(",", start)
    task_id = int(row[start:end])

    change_status(task_id)
    table.set(row, 'Status', 'completed')

    messagebox.showinfo("Success", "Status changed successfully!")

status_button = ttk.Button(root, text="Mark as done", command=on_status_click)
status_button.place(x=230, y=105)

# treeview
table = ttk.Treeview(root, columns=("Course", "Assignment", "Due Date", "Priority", "Status"), show = "headings", height=8)

style = ttk.Style()
style.configure("Treeview", foreground="black")

table.heading("Course", text="Course")
table.column("Course", width=75)

table.heading("Assignment", text="Assignment")
table.column("Assignment", width=175)

table.heading("Due Date", text="Due Date")
table.column("Due Date", width=100)

table.heading("Priority", text="Priority")
table.column("Priority", width=75)

table.heading("Status", text="Status")
table.column("Status", width=75)

table.place(x=50, y=140)

# filtering
filter_label = ttk.Label(root, text="Filter by:")
filter_label.place(x=50, y=351)

def filter_by_priority(event):
    item = filter_priority.get()

    session = Session()

    all_tasks = session.query(Task).all()

    table.tag_configure("Low", background="#00FF08")      
    table.tag_configure("Medium", background="#FFE600")   
    table.tag_configure("High", background="#FF0019")  

    if item == "None":
        refresh_table()
    else:
        for task in table.get_children():
            table.delete(task)

        for task in all_tasks:
            if item in task.priority:
                table.insert("", "end", values=(task.course, task.assignment, task.due_date, task.priority, task.status), tags=(task.priority,))

    filter_status.set("None")

    session.close()

priority_label = ttk.Label(root, text="Priority")
priority_label.place(x=200, y=330)

filter_priority = ttk.Combobox(root, values=["None", "Low", "Medium", "High"], state="readonly", width=9)
filter_priority.set("None")
filter_priority.bind("<<ComboboxSelected>>", filter_by_priority)
filter_priority.place(x=170, y=350)

def filter_by_status(event):
    item = filter_status.get()

    session = Session()

    all_tasks = session.query(Task).all()

    table.tag_configure("Low", background="#00FF08")      
    table.tag_configure("Medium", background="#FFE600")   
    table.tag_configure("High", background="#FF0019")  

    if item == "None":
        refresh_table()
    else:
        for task in table.get_children():
            table.delete(task)

        for task in all_tasks:
            if item in task.status:
                table.insert("", "end", values=(task.course, task.assignment, task.due_date, task.priority, task.status), tags=(task.priority))

    filter_priority.set("None")

    session.close()

status_label = ttk.Label(root, text="Status")
status_label.place(x=335, y=330)

filter_status = ttk.Combobox(root, values=["None", "completed", "pending"], state="readonly", width=10)
filter_status.set("None")
filter_status.bind("<<ComboboxSelected>>", filter_by_status)
filter_status.place(x=305, y=350)

def nuke():
    session = Session()

    all_tasks = session.query(Task).all()
    
    for item in all_tasks:
        delete_task(item.id)

    session.close()

    messagebox.showinfo("NUKED", "Database has been nuked!")

    refresh_table()

clear_button = ttk.Button(root, text="Nuke", command=nuke)
clear_button.place(x=475, y=348)

def on_app_launch():
    session = Session()

    all_tasks = session.query(Task).all()

    date = f"{dt.datetime.now():%m/%-d/%y}"
    match = False

    msg = "Task(s) due today: \n"

    for task in all_tasks:
        if task.due_date == date:
            msg += f"- {task.course}: {task.assignment}\n"
            match = True
            
    if match:
        messagebox.showinfo("Reminder", msg) 

def refresh_table():
    session = Session()

    all_tasks = session.query(Task).all()

    table.tag_configure("Low", background="#00FF08")      
    table.tag_configure("Medium", background="#FFE600")   
    table.tag_configure("High", background="#FF0019")  

    for row in table.get_children():
        table.delete(row)

    for task in all_tasks:
        table.insert("", tk.END, text="", iid=str(task), values=(task.course, task.assignment, task.due_date, task.priority, task.status), tags=(task.priority,))

on_app_launch()
refresh_table()

root.mainloop()