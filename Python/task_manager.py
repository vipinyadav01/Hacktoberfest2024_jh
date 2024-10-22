import json
from datetime import datetime, date

class Task:
    def __init__(self, title, description, due_date=None, completed=False):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(data["title"], data["description"])
        task.completed = data["completed"]
        if data["due_date"]:
            task.due_date = datetime.fromisoformat(data["due_date"]).date()
        return task

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                return [Task.from_dict(task_data) for task_data in data]
        except FileNotFoundError:
            return []

    def save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=2)

    def add_task(self, title, description, due_date=None):
        task = Task(title, description, due_date)
        self.tasks.append(task)
        self.save_tasks()

    def list_tasks(self):
        return self.tasks

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
            self.save_tasks()
            return True
        return False

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()
            return True
        return False

def print_tasks(tasks):
    for i, task in enumerate(tasks):
        status = "✓" if task.completed else " "
        due = f"(Due: {task.due_date})" if task.due_date else ""
        print(f"[{status}] {i+1}. {task.title} {due}")
        print(f"   {task.description}")

def main():
    manager = TaskManager()

    while True:
        print("\n--- Task Manager ---")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Complete Task")
        print("4. Remove Task")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            due_date_str = input("Enter due date (YYYY-MM-DD) or leave blank: ")
            due_date = None
            if due_date_str:
                try:
                    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                except ValueError:
                    print("Invalid date format. Task will be created without a due date.")
            manager.add_task(title, description, due_date)
            print("Task added successfully!")

        elif choice == "2":
            tasks = manager.list_tasks()
            if tasks:
                print_tasks(tasks)
            else:
                print("No tasks found.")

        elif choice == "3":
            tasks = manager.list_tasks()
            if tasks:
                print_tasks(tasks)
                index = int(input("Enter the number of the task to complete: ")) - 1
                if manager.complete_task(index):
                    print("Task marked as completed!")
                else:
                    print("Invalid task number.")
            else:
                print("No tasks found.")

        elif choice == "4":
            tasks = manager.list_tasks()
            if tasks:
                print_tasks(tasks)
                index = int(input("Enter the number of the task to remove: ")) - 1
                if manager.remove_task(index):
                    print("Task removed successfully!")
                else:
                    print("Invalid task number.")
            else:
                print("No tasks found.")

        elif choice == "5":
            print("Thank you for using Task Manager. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
