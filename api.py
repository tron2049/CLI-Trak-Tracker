import json
import os 
from datetime import datetime

class TaskManager():
    def __init__(self,filename="Tasks"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)
                

    def load_tasks(self):
        try:
            with open(self.filename, "r") as f:
                tasks = json.load(f)
                return tasks
        except Exception as e:
            print(f"Error loading tasks: {e}")
            return []

    def save_tasks(self, tasks):
        with open(self.filename, "w") as f:
            json.dump(tasks, f, indent=4)
            return
        

    def add_task(self, title, status="incomplete"):
        tasks = self.load_tasks()
        id = max([t["id"] for t in tasks], default=0) + 1
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_task = {
            "id": id,
            "name": title,
            "status": status,
            "date": date
        }
        tasks.append(new_task)
        self.save_tasks(tasks)
        return new_task

    def update_task(self, id: int, title: str, status: str):
        tasks = self.load_tasks()
        for task in tasks:
            if id == task["id"]:
                if title is not None:
                    task["name"] = title
                if status is not None:
                    task["status"] = status
                self.save_tasks(tasks)
                return task
        return None

    def delete_task(self, id: int):
        tasks = self.load_tasks()
        for task in tasks:
            if id == task["id"]:
                tasks.remove(task)
                self.save_tasks(tasks)
                return task
        return None

  
    def list_tasks(self, id=None, status=None):
        tasks = self.load_tasks()
        if id is not None:
            tasks = [t for t in tasks if t["id"] == id]
    
        if status is not None:
            tasks = [t for t in tasks if t["status"] == status]
        return tasks
