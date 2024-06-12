class TaskView:
    @staticmethod
    def display_menu():
        print("\nTask Manager")
        print("1. Add Task")
        print("2. Delete Task")
        print("3. Mark Task as Completed")
        print("4. view All Tasks")
        print("5. view Completed Tasks")
        print("6. view Pending Tasks")
        print("7. Exit")

    @staticmethod
    def get_user_choice():
        return input("Enter your choice: ")

    @staticmethod
    def get_task_description():
        return input("Enter task description: ")

    @staticmethod
    def get_task_index(action):
        return int(input(f"Enter task index to {action}: ")) - 1

    @staticmethod
    def display_tasks(tasks):
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task}")

    @staticmethod
    def display_invalid_choice():
        print("Invalid choice. Please try again.")
