import tkinter as tk
from tkinter import ttk

# primary window settings
root = tk.Tk()
root.title("PriorityManager")
root.geometry("450x650+700+200")

title = ttk.Label(root, text="PriorityManager", font=("Arial", 24))
title.pack(padx=20,pady=20)

table = ttk.Treeview(columns=("ID", "Course", "Assignment", "Due Date", "Priority"))
# table.heading("ID", text="ID")
table.pack()

root.mainloop()