import datetime
import json
import os

class Task:
    def __init__(self, title, due_date, priority, tags, recurring=False, progress=0, completed=False):
        self.title = title
        self.due_date = due_date
        self.priority = priority
        self.tags = tags
        self.recurring = recurring
        self.progress = progress
        self.completed = completed

    def to_dict(self):
        return {
            "title": self.title,
            "due_date": self.due_date.isoformat(),
            "priority": self.priority,
            "tags": self.tags,
            "recurring": self.recurring,
            "progress": self.progress,
            "completed": self.completed
        }

class TodoList:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as f:
                tasks_data = json.load(f)
                for task_data in tasks_data:
                    task = Task(
                        title=task_data["title"],
                        due_date=datetime.datetime.fromisoformat(task_data["due_date"]),
                        priority=task_data["priority"],
                        tags=task_data["tags"],
                        recurring=task_data["recurring"],
                        progress=task_data["progress"],
                        completed=task_data.get("completed", False)  # Default to False if not present
                    )
                    self.tasks.append(task)

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f)

    def add_task(self, title, due_date, priority, tags, recurring=False):
        task = Task(title, due_date, priority, tags, recurring)
        self.tasks.append(task)
        self.save_tasks()

    def edit_task(self, index, title, due_date, priority, tags, recurring=False):
        if 0 <= index < len(self.tasks):
            task = self.tasks[index]
            task.title = title
            task.due_date = due_date
            task.priority = priority
            task.tags = tags
            task.recurring = recurring
            self.save_tasks()

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
            self.save_tasks()

    def list_tasks(self):
        return [(task.title, task.due_date, task.priority, task.tags, task.progress, task.completed) for task in self.tasks]