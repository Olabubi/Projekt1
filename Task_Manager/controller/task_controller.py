from Task_Manager.model.task_model import TaskManager
from Task_Manager.view.tkinter_view import TkinterView

class TaskController:
    def __init__(self):
        self.manager = TaskManager()
        self.view = TkinterView(self)

    def add_task(self, description, due_date, priority):
        self.manager.add_task(description, due_date, priority)

    def delete_task(self, index):
        self.manager.delete_task(index)

    def mark_task_completed(self, index):
        self.manager.mark_task_completed(index)

    def unmark_task_completed(self, index):
        self.manager.unmark_task_completed(index)

    def view_tasks(self, completed=None):
        return self.manager.view_tasks(completed)

    def export_tasks_to_excel(self):
        # Get the sorted tasks from the controller
        tasks = self.manager.view_tasks()
        self.manager.export_to_excel(tasks)

    def export_tasks_to_pdf(self):
        tasks = self.manager.view_tasks()
        self.manager.export_to_pdf(tasks)

    def filter_tasks(self, completion_status, priority):
        tasks = self.manager.view_tasks()
        if completion_status != 'All':
            tasks = [task for task in tasks if (task.completed and completion_status == 'Completed') or (not task.completed and completion_status == 'Pending')]
        if priority != 'All':
            tasks = [task for task in tasks if task.priority == priority]
        return tasks

    def get_task(self, index):
        return self.manager.tasks[index]

    def cancel_task(self, index):
        self.manager.cancel_task(index)

    def change_due_date(self, index, new_due_date):
        self.manager.change_due_date(index, new_due_date)

    def run(self):
        self.view.run()
