import cmd
import os


class TaskTrackerCLI(cmd.Cmd):
    prompt = "(task-tracker) >>"
    intro = "Welcome to your Task Tracker. Type help to list commands."

    def __init__(self):
        super().__init__()
        self.current_directory = os.getcwd()
        
    def do_ls(self, arg):
        """List all tasks in the current directory."""
        try:
            tasks = os.listdir(self.current_directory)
            if tasks:
                print("Tasks:")
                for task in tasks:
                    print(f"- {task}")
            else:
                print("No tasks found.")
        except Exception as e:
            print(f"Error listing tasks: {e}")
