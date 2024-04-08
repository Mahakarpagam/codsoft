import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        
        self.conn = sqlite3.connect('todo.db')
        self.c = self.conn.cursor()
        self.create_table()
        
        self.tasks = []
        
        self.task_title_var = tk.StringVar()
        self.task_desc_var = tk.StringVar()
        
        self.create_widgets()
        self.load_tasks()
    
    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS tasks 
                          (id INTEGER PRIMARY KEY, title TEXT, description TEXT, priority TEXT, due_date TEXT, completed INTEGER)''')
        self.conn.commit()
    
    def create_widgets(self):
        self.task_frame = tk.Frame(self.root)
        self.task_frame.pack(padx=10, pady=10)
        
        self.task_title_entry = tk.Entry(self.task_frame, textvariable=self.task_title_var, width=40)
        self.task_title_entry.grid(row=0, column=0, padx=5, pady=5)
        
        self.add_task_btn = tk.Button(self.task_frame, text="Add Task", command=self.add_task)
        self.add_task_btn.grid(row=0, column=1, padx=5, pady=5)
        
        self.task_listbox = tk.Listbox(self.root, width=60, height=15)
        self.task_listbox.pack(padx=10, pady=10)
        
        self.load_tasks()
        self.task_listbox.bind("<Double-Button-1>", self.edit_task)
        self.task_listbox.bind("<Delete>", self.delete_task)
    
    def add_task(self):
        title = self.task_title_var.get()
        if title:
            priority = "Normal"
            due_date = datetime.now().strftime("%Y-%m-%d")
            self.c.execute('''INSERT INTO tasks (title, description, priority, due_date, completed) VALUES (?, ?, ?, ?, ?)''',
                            (title, "", priority, due_date, 0))
            self.conn.commit()
            self.load_tasks()
            self.task_title_var.set("")
        else:
            messagebox.showwarning("Warning", "Please enter a task title.")
    
    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        self.tasks = []
        self.c.execute('''SELECT * FROM tasks''')
        rows = self.c.fetchall()
        for row in rows:
            task = {
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'priority': row[3],
                'due_date': row[4],
                'completed': row[5]
            }
            self.tasks.append(task)
            self.task_listbox.insert(tk.END, f"{task['title']} - {task['priority']} - {task['due_date']} - {'Completed' if task['completed'] else 'Active'}")
    
    def edit_task(self, event):
        if self.task_listbox.curselection():
            index = self.task_listbox.curselection()[0]
            task = self.tasks[index]
            title = task['title']
            description = task['description']
            priority = task['priority']
            due_date = task['due_date']
            completed = task['completed']
            
            self.task_title_var.set(title)
            if description:
                self.task_desc_var.set(description)
            else:
                self.task_desc_var.set("")
            self.add_task_btn.config(text="Update Task", command=lambda: self.update_task(task['id']))
    
    def update_task(self, task_id):
        title = self.task_title_var.get()
        description = self.task_desc_var.get()
        if title:
            self.c.execute('''UPDATE tasks SET title=?, description=? WHERE id=?''', (title, description, task_id))
            self.conn.commit()
            self.load_tasks()
            self.task_title_var.set("")
            self.task_desc_var.set("")
            self.add_task_btn.config(text="Add Task", command=self.add_task)
        else:
            messagebox.showwarning("Warning", "Please enter a task title.")
    
    def delete_task(self, event):
        if self.task_listbox.curselection():
            index = self.task_listbox.curselection()[0]
            task_id = self.tasks[index]['id']
            self.c.execute('''DELETE FROM tasks WHERE id=?''', (task_id,))
            self.conn.commit()
            self.load_tasks()

def run_app():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

run_app()
