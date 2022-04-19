import sys

from PyQt5.QtWidgets import *

from controller.task_list import get_task_list, get_task_lists, create_task_list, delete_task_list
from controller.task import create_task, update_task, delete_task


class TaskListWidget(QWidget):
    def __init__(self, task_list):
        QWidget.__init__(self)
        self.task_list = task_list
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.title = QLabel(task_list.title)
        self.task_list_widget = QListWidget()
        self.tasks = dict()

        self.input_add_task = QLineEdit()
        self.button_add_task = QPushButton("Add Task")
        self.button_delete_task_list = QPushButton("Delete List")
        self.button_change_name = QPushButton("Change Title")
        self.button_delete_selected = QPushButton("Delete Selected")
        self.button_mark_selected_as_done = QPushButton("Mark as Done")

        self.button_delete_task_list.clicked.connect(self.kill)
        self.button_add_task.clicked.connect(self.add_task)
        self.button_delete_selected.clicked.connect(self.delete_selected)
        self.button_mark_selected_as_done.clicked.connect(self.mark_selected_as_done)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.task_list_widget)
        self.layout.addWidget(self.input_add_task)
        self.layout.addWidget(self.button_add_task)
        self.layout.addWidget(self.button_mark_selected_as_done)
        self.layout.addWidget(self.button_delete_selected)
        self.layout.addWidget(self.button_delete_task_list)

        self.update()

    def kill(self):
        delete_task_list(self.task_list.entity_id)
        self.setParent(None)

    def update(self):
        self.task_list = get_task_list(task_list_id=self.task_list.entity_id)
        print(self.task_list)
        self.title.setText(self.task_list.title)
        tasks = [t for t in self.task_list.tasks if not t.done] + [t for t in self.task_list.tasks if t.done]
        self.task_list_widget.clear()
        self.tasks = dict()
        for i, task in enumerate(tasks):
            self.tasks[i] = task
            self.task_list_widget.insertItem(i, f"DONE - {task.description}" if task.done else task.description)

    def add_task(self):
        create_task(self.input_add_task.text(), self.task_list.entity_id)
        self.input_add_task.setText("")
        self.update()

    def delete_selected(self):
        selected_items = self.task_list_widget.selectedItems()
        for item in selected_items:
            item_row = [row for row in range(len(self.tasks)) if self.task_list_widget.item(row) is item][0]
            task = self.tasks[item_row]
            delete_task(task.entity_id)
        self.update()

    def mark_selected_as_done(self):
        selected_items = self.task_list_widget.selectedItems()
        for item in selected_items:
            item_row = [row for row in range(len(self.tasks)) if self.task_list_widget.item(row) is item][0]
            task = self.tasks[item_row]
            update_task(task.entity_id, done=True)
        self.update()


class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.task_lists = dict()
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.init_ui()

    def add_new_list(self):
        title, ok = QInputDialog.getText(self, 'Create List',
                                         'Enter task list title')
        if ok:
            new_task_list = create_task_list(title)
            self.add_task_list_ui(new_task_list)

    def add_task_list_ui(self, task_list):
        self.task_lists[task_list.title] = TaskListWidget(task_list)
        self.layout.addWidget(self.task_lists[task_list.title])

    def init_ui(self):
        button_add_list = QPushButton("Add new list")
        self.layout.addWidget(button_add_list)
        button_add_list.clicked.connect(self.add_new_list)
        for task_list in get_task_lists():
            self.add_task_list_ui(task_list)

    def clicked(self, qmodelindex):
        item = self.listwidget.currentItem()
