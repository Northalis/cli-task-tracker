import cmd
import os
import json
from datetime import datetime

task_file = "tasks.json"


class TaskyCLI(cmd.Cmd):
    prompt = "(tasky) >> "
    intro = "Welcome to your Tasky. Type help to list commands."

    def __init__(self):
        super().__init__()
        self.current_directory = os.getcwd()

    def load_tasks(self):
        """Load tasks from the JSON file."""
        if os.path.exists(task_file):
            with open(task_file, "r") as f:
                return json.load(f)
        return []

    def save_tasks(self, tasks):
        """Save tasks to the JSON file."""
        with open(task_file, "w") as f:
            json.dump(tasks, f)

    def do_list(self, status: str = ""):
        """List all tasks. can filter by status: list [status] -- > status can be 'todo', 'in-progress', or 'done'"""
        tasks = self.load_tasks()
        if not tasks:
            print("No tasks found.")
            return

        print(f" ID   Description         Status        CreatedAt          UpdatedAt")
        print("-" * 70)

        if status:
            """Filter tasks by status if provided"""
            filtered_tasks = [
                task for task in tasks if task["status"].lower() == status.lower()
            ]
            tasks = filtered_tasks

            for task in tasks:
                print(
                    f" {task['id']}     {task['description']:<15}     {task['status']:<12}    {task['createdAt']}    {task['updatedAt']}"
                )
            return

        """ Print each task w/ details"""

        for task in tasks:

            print(
                f" {task['id']}     {task['description']:<15}     {task['status']:<12}    {task['createdAt']}    {task['updatedAt']}"
            )

    def do_add(self, description: str):
        """Add a new task: add <description>"""
        tasks = self.load_tasks()

        if not description:
            print("Please provide a task description.")
            return
        """
        Task properties:
        - id: Unique identifier for the task
        - description: Description of the task
        - status: Current status of the task (e.g., To do, In progress, Done)
        """
        task = {
            "id": len(tasks) + 1,
            "description": description,
            "status": "todo",
            "createdAt": datetime.now().isoformat("#", "seconds"),
            "updatedAt": datetime.now().isoformat("#", "seconds"),
        }
        """ append new task to list of tasks"""
        tasks.append(task)
        """ Save the updated tasks to the JSON file """
        self.save_tasks(tasks)

        print(f"Task added: {description}")

    def do_update(self, line):
        """Update a task's status: update <id> <status> --> status can be 'todo', 'in-progress', or 'done'"""
        args = line.split()
        if len(args) != 2:
            print("Usage: update <id> <status>")
            return

        task_id, status = args
        tasks = self.load_tasks()
        task_id = int(task_id)
        new_status = status.lower()
        valid_statuses = ["todo", "in-progress", "done"]
        if new_status not in valid_statuses:
            print(f"Invalid status. Valid statuses are: {', '.join(valid_statuses)}")
            return

        """ Find the task by ID and update its status """
        for task in tasks:
            if task["id"] == task_id:
                task["status"] = new_status
                task["updatedAt"] = datetime.now().isoformat("#", "seconds")
                break
        else:
            print(f"Task with ID {task_id} not found.")
            return

        """ Save the updated tasks to the JSON file """
        self.save_tasks(tasks)

        print(f"Task {task_id} updated to '{new_status}'.")

    def do_delete(self, task_id):
        """Delete a task by ID: delete <id>"""
        tasks = self.load_tasks()

        if not task_id:
            print("Please provide a task ID to delete.")
            return

        try:
            task_id = int(task_id)
        except ValueError:
            print("Invalid task ID. Please provide a numeric ID.")
            return

        """ Find the task by ID and remove it """
        for i, task in enumerate(tasks):
            if task["id"] == task_id:
                del tasks[i]
                print(f"Task {task_id} deleted.")
                break
        else:
            print(f"Task with ID {task_id} not found.")
            return

        for task in tasks:
            if task["id"] > task_id:
                task["id"] -= 1
                task["updatedAt"] = datetime.now().isoformat("#", "seconds")

        """ Save the updated tasks to the JSON file """
        self.save_tasks(tasks)

    def do_quit(self, line):
        """Exit the Tasky CLI."""
        print("Closing Tasky. Goodbye!")
        return True


if __name__ == "__main__":
    TaskyCLI().cmdloop()
