import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel
from tkinter import ttk
from todo_list import TodoList
import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("600x600")  # Adjusted height for more space

        self.todo_list = TodoList()

        self.task_listbox = tk.Listbox(root, width=70, height=20)  # Width and height for the listbox
        self.task_listbox.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        self.edit_button = tk.Button(root, text="Edit Task", command=self.edit_task)
        self.edit_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.complete_button = tk.Button(root, text="Complete Task", command=self.complete_task)
        self.complete_button.pack(pady=5)

        self.sort_button = tk.Button(root, text="Sort Tasks", command=self.sort_tasks)
        self.sort_button.pack(pady=5)

        self.refresh_button = tk.Button(root, text="Refresh Tasks", command=self.refresh_tasks)
        self.refresh_button.pack(pady=5)

        self.refresh_tasks()

    def add_task(self):
        title = simpledialog.askstring("Task Title", "Enter the task title:")
        due_date_str = simpledialog.askstring("Due Date", "Enter due date (YYYY-MM-DD):")
        priority = self.select_priority("Select Priority")
        tags = self.select_tags("Select Tags")
        
        if title and due_date_str and priority:
            try:
                due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d")
                tags_list = [tag.strip() for tag in tags.split(",")] if tags else []
                self.todo_list.add_task(title, due_date, priority, tags_list)
                self.refresh_tasks()
            except ValueError:
                messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")

    def edit_task(self):
        selected_task_index = self.task_listbox.curselection()
        if not selected_task_index:
            messagebox.showwarning("Select Task", "Please select a task to edit.")
            return
        index = selected_task_index[0]
        task = self.todo_list.tasks[index]

        title = simpledialog.askstring("Task Title", "Enter the new task title:", initialvalue=task.title)
        due_date_str = simpledialog.askstring("Due Date", "Enter new due date (YYYY-MM-DD):", initialvalue=task.due_date.date().isoformat())
        priority = self.select_priority("Select Priority", initial_value=task.priority)
        tags = self.select_tags("Select Tags", initial_value=", ".join(task.tags))
        
        if title and due_date_str and priority:
            try:
                due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d")
                tags_list = [tag.strip() for tag in tags.split(",")] if tags else []
                self.todo_list.edit_task(index, title, due_date, priority, tags_list)
                self.refresh_tasks()
            except ValueError:
                messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if not selected_task_index:
            messagebox.showwarning("Select Task", "Please select a task to delete.")
            return
        index = selected_task_index[0]
        self.todo_list.delete_task(index)
        self.refresh_tasks()

    def complete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if not selected_task_index:
            messagebox.showwarning("Select Task", "Please select a task to complete.")
            return
        index = selected_task_index[0]
        self.todo_list.complete_task(index)
        self.refresh_tasks()

    def sort_tasks(self):
        sort_option = simpledialog.askstring("Sort Tasks", "Sort by (title, due date, priority, event):").strip().lower()
        if sort_option in ["title", "due date", "priority", "event"]:
            self.todo_list.tasks.sort(key=lambda x: (x.title if sort_option == "title" else 
                                                       x.due_date if sort_option == "due date" else 
                                                       x.priority if sort_option == "priority" else 
                                                       x.title))  # 'event' corresponds to title
            self.refresh_tasks()
        else:
            messagebox.showwarning("Invalid Option", "Please enter a valid sort option (title, due date, priority, event).")

    def select_priority(self, title, initial_value=None):
        priority_window = Toplevel(self.root)
        priority_window.title(title)

        priority_var = tk.StringVar(value=initial_value if initial_value else "Medium")

        tk.Label(priority_window, text="Select a priority:").pack(pady=5)

        priorities = ["High", "Medium", "Low"]
        for priority in priorities:
            rb = tk.Radiobutton(priority_window, text=priority, variable=priority_var, value=priority)
            rb.pack(anchor="w")

        confirm_button = tk.Button(priority_window, text="OK", command=priority_window.destroy)
        confirm_button.pack(pady=10)

        priority_window.wait_window(priority_window)
        return priority_var.get()

    def select_tags(self, title, initial_value=None):
        tags_window = Toplevel(self.root)
        tags_window.title(title)

        tag_var = tk.StringVar(value=initial_value if initial_value else "")

        tk.Label(tags_window, text="Select or add tags:").pack(pady=5)

        # Example predefined tags
        predefined_tags = ["Work", "Personal", "Urgent"]

        # Create Combobox for selecting predefined tags
        tags_combobox = ttk.Combobox(tags_window, textvariable=tag_var, values=predefined_tags)
        tags_combobox.pack(pady=5)

        # Entry for custom tags
        custom_tag_entry = tk.Entry(tags_window)
        custom_tag_entry.pack(pady=5)
        custom_tag_entry.insert(0, "Enter custom tag")

        def add_custom_tag():
            custom_tag = custom_tag_entry.get().strip()
            if custom_tag and custom_tag not in predefined_tags:
                predefined_tags.append(custom_tag)
                tags_combobox['values'] = predefined_tags  # Update Combobox values
                tags_combobox.set(custom_tag)  # Set to the new custom tag
                custom_tag_entry.delete(0, tk.END)  # Clear the entry

        add_custom_button = tk.Button(tags_window, text="Add Custom Tag", command=add_custom_tag)
        add_custom_button.pack(pady=5)

        confirm_button = tk.Button(tags_window, text="OK", command=tags_window.destroy)
        confirm_button.pack(pady=10)

        tags_window.wait_window(tags_window)
        return tag_var.get()

    def refresh_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.todo_list.list_tasks()
        for task in tasks:
            status = "[✓]" if task[5] else "[ ]"
            self.task_listbox.insert(tk.END, f"{status} {task[0]} - Due: {task[1].date()} - Priority: {task[2]} - Tags: {', '.join(task[3])} - Progress: {task[4]}%")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()