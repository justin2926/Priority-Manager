import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from database import *

# primary window settings
root = tk.Tk()
root.title("PriorityManager")
# root.geometry("500x700+700+200") # 700 + 200 for 14" MBP display (450x650)

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

priority_dropdown = ttk.Combobox(root, values=['Low','Medium','High'])
priority_dropdown.pack(padx=10, pady=2)

# add button
add_button = ttk.Button(root, text="Add")
add_button.place(x=50, y=20)
add_button.pack(padx=10, pady=2)

# remove button
remove_button = ttk.Button(root, text="Remove")
remove_button.pack(padx=10, pady=2)

# treeview
table = ttk.Treeview(root, columns=("Course", "Assignment", "Due Date", "Priority"), show = "headings")
table.heading("Course", text="Course")
table.heading("Assignment", text="Assignment")
table.heading("Due Date", text="Due Date")
table.heading("Priority", text="Priority")
table.pack(padx=50, pady=5)


root.mainloop()