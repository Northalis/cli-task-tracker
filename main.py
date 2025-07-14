import cmd
import os


class TaskTrackerCLI(cmd.Cmd):
    prompt = "(task-tracker) >>"
    intro = "Welcome to your Task Tracker. Type help to list commands."

    def __init__(self):
        super().__init__()
        self.current_directory = os.getcwd()
