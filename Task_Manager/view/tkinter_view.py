import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from datetime import datetime

class TkinterView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Task Manager")

        # obrazek checkbox i dostosowanie rozmiaru
        self.checked_image = ImageTk.PhotoImage(Image.open("checked.png").resize((20, 20)))
        self.unchecked_image = ImageTk.PhotoImage(Image.open("unchecked.png").resize((20, 20)))
        self.images = [self.checked_image, self.unchecked_image]  # Keep references to images

        self.task_mapping = {}
        self.sort_order = {col: 'asc' for col in range(4)}
        self.task_data = []

        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10, fill='x')

        # pola zadań
        self.description_entry = tk.Entry(self.frame, width=50)
        self.description_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(self.frame, text="Description:").grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.due_date_entry = DateEntry(self.frame, width=12, background='darkblue', foreground='white',
                                        borderwidth=2, date_pattern='dd/mm/yyyy')
        self.due_date_entry.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
        tk.Label(self.frame, text="Due Date:").grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.priority_var = tk.StringVar(value='Low')
        self.priority_menu = tk.OptionMenu(self.frame, self.priority_var, 'Low', 'Medium', 'High')
        self.priority_menu.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')
        tk.Label(self.frame, text="Priority:").grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

        # Task przyciski
        self.add_button = tk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        # filrty
        self.filter_frame = tk.Frame(self.root)
        self.filter_frame.pack(padx=1, pady=1, fill='x')

        tk.Label(self.filter_frame, text="Filter by Completion:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_completion_var = tk.StringVar(value='All')
        self.filter_completion_menu = tk.OptionMenu(self.filter_frame, self.filter_completion_var, 'All', 'Completed',
                                                    'Pending')
        self.filter_completion_menu.grid(row=0, column=1, pady=5)

        tk.Label(self.filter_frame, text="Filter by Priority:").grid(row=0, column=2, padx=(50, 5), pady=5)
        self.filter_priority_var = tk.StringVar(value='All')
        self.filter_priority_menu = tk.OptionMenu(self.filter_frame, self.filter_priority_var, 'All', 'Low', 'Medium',
                                                  'High')
        self.filter_priority_menu.grid(row=0, column=3, pady=5)

        self.apply_filter_button = tk.Button(self.filter_frame, text="Apply Filter", command=self.apply_filters)
        self.apply_filter_button.grid(row=0, column=4, columnspan=2, padx=50, pady=5)

        # lista zadań
        self.task_tree = ttk.Treeview(self.root, columns=("Description", "Due Date", "Priority", "Completed Date"))
        self.task_tree.heading("#0", text="Checkbox", anchor=tk.CENTER)
        self.task_tree.heading("Description", text="Description", anchor=tk.CENTER)
        self.task_tree.heading("Due Date", text="Due Date", anchor=tk.CENTER)
        self.task_tree.heading("Priority", text="Priority", anchor=tk.CENTER)
        self.task_tree.heading("Completed Date", text="Completed Date", anchor=tk.CENTER)
        self.task_tree.column("#0", width=70, anchor=tk.CENTER)
        self.task_tree.column("Description", width=200, anchor=tk.CENTER)
        self.task_tree.column("Due Date", width=100, anchor=tk.CENTER)
        self.task_tree.column("Priority", width=100, anchor=tk.CENTER)
        self.task_tree.column("Completed Date", width=150, anchor=tk.CENTER)
        self.task_tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.task_tree.bind("<Double-1>", self.toggle_task_completion)
        self.task_tree.bind("<Button-3>", self.show_popup_menu)
        self.description_entry.bind("<Return>", self.add_task)

        # sortowanie po nagłówkaach
        for col, header in enumerate(("Description", "Due Date", "Priority", "Completed Date")):
            self.task_tree.heading(col, text=header, command=lambda c=col: self.sort_tasks(c))

        # przyciski do exportów
        self.export_excel_button = tk.Button(self.root, text="Export to Excel", command=self.export_to_excel)
        self.export_excel_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.export_pdf_button = tk.Button(self.root, text="Export to PDF", command=self.export_to_pdf)
        self.export_pdf_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.new_due_date = None
        self.selected_item_id = None

        self.refresh_tasks()


    def add_task(self, event=None):
        description = self.description_entry.get()
        due_date = self.due_date_entry.get()
        priority = self.priority_var.get()
        if description:
            self.controller.add_task(description, due_date, priority)
            self.description_entry.delete(0, tk.END)
            self.refresh_tasks()
        else:
            messagebox.showwarning("Input Error", "Task description cannot be empty")

    def export_to_excel(self):
        self.controller.export_tasks_to_excel()
        messagebox.showinfo("Export Complete", "Tasks exported to Excel successfully.")

    def export_to_pdf(self):
        self.controller.export_tasks_to_pdf()
        messagebox.showinfo("Export Complete", "Tasks exported to PDF successfully.")

    def delete_task(self, event=None):
        selected_item = self.task_tree.selection()
        if selected_item:
            item_id = selected_item[0]
            index = self.task_mapping.get(item_id)
            self.controller.delete_task(index)
            self.refresh_tasks()
        else:
            messagebox.showwarning("Selection Error", "No task selected")

    def toggle_task_completion(self, event):
        selected_item = self.task_tree.selection()
        if selected_item:
            item_id = selected_item[0]
            index = self.task_mapping.get(item_id)
            task = self.controller.get_task(index)
            if task.completed:
                self.controller.unmark_task_completed(index)
            else:
                self.controller.mark_task_completed(index)
            self.refresh_tasks()

    def show_popup_menu(self, event):
        selected_item = self.task_tree.selection()
        if selected_item:
            item_id = selected_item[0]
            index = self.task_mapping.get(item_id)
            task = self.controller.get_task(index)
            self.selected_item_id = item_id
            popup_menu = tk.Menu(self.root, tearoff=0)
            popup_menu.add_command(label='Delete Task', command=self.delete_task)
            popup_menu.add_command(label="Change Due Date", command=self.change_due_date)
            popup_menu.post(event.x_root, event.y_root)

    def change_due_date(self):
        if self.selected_item_id:
            index = self.task_mapping.get(self.selected_item_id)
            if index is not None:
                task = self.controller.get_task(index)
                new_due_date_window = tk.Toplevel(self.root)
                new_due_date_window.title("Change Due Date")
                tk.Label(new_due_date_window, text="New Due Date:").pack(padx=10, pady=5)
                self.new_due_date_entry = DateEntry(new_due_date_window, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
                self.new_due_date_entry.pack(padx=10, pady=5)
                tk.Button(new_due_date_window, text="Change", command=lambda: self.apply_new_due_date(index, new_due_date_window)).pack(pady=10)

    def apply_new_due_date(self, index, window):
        new_due_date = self.new_due_date_entry.get()
        self.controller.change_due_date(index, new_due_date)
        window.destroy()
        self.refresh_tasks()

    def apply_filters(self):
        completion_status = self.filter_completion_var.get()
        priority = self.filter_priority_var.get()
        filtered_tasks = self.controller.filter_tasks(completion_status, priority)
        self.display_tasks(filtered_tasks)

    def refresh_tasks(self):
        tasks = self.controller.view_tasks()
        self.display_tasks(tasks)

    def display_tasks(self, tasks):
        # Clear existing items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        # Display tasks
        for index, task in enumerate(tasks):
            checkbox_image = self.checked_image if task.completed else self.unchecked_image
            item_id = self.task_tree.insert("", index, text="", values=(task.description, task.due_date, task.priority, task.completion_date), image=checkbox_image)
            self.task_mapping[item_id] = index

    def sort_tasks(self, col):
        order = self.sort_order[col]
        reverse = True if order == 'asc' else False
        self.task_data = [(self.task_tree.set(k, col), k) for k in self.task_tree.get_children('')]
        self.task_data.sort(reverse=reverse)
        for index, (val, k) in enumerate(self.task_data):
            self.task_tree.move(k, '', index)
        self.sort_order[col] = 'desc' if order == 'asc' else 'asc'

    def run(self):
        self.root.mainloop()
