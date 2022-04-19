from enum import Enum

from controller.task_list import get_task_list, get_task_lists, create_task_list, delete_task_list
from controller.task import get_tasks, create_task, update_task, delete_task


class State(Enum):
    LISTS_SHOW = 1
    LIST_OPTIONS = 2
    TASKS_SHOW = 3
    TASK_OPTIONS = 4


def run_alpha():
    chosen_list = None
    chosen_task = None
    command = ""
    current_state = State.LISTS_SHOW
    while command != "stop":
        if current_state == State.LISTS_SHOW:
            print("Lists:\n")
            task_lists = get_task_lists()
            string = "\n".join([f'{i} - {task_list.title}' for i, task_list in enumerate(task_lists)])
            print(string)
            command = input("Choose list by number (-1 - add new): ")
            if command == "-1":
                list_name = input("Name of new list: ")
                create_task_list(list_name)
            elif command != "stop":
                current_state = State.LIST_OPTIONS
                chosen_list = int(command)
        elif current_state == State.LIST_OPTIONS:
            print(f"{task_lists[chosen_list].title} options:"
                  "\n\t 1 - Show list"
                  "\n\t 2 - Delete list"
                  "\n\t 3 - Back")
            command = input("Enter options: ")
            if command == "1":
                current_state = State.TASKS_SHOW
            elif command == "2":
                delete_task_list(task_lists[chosen_list].entity_id)
                current_state = State.LISTS_SHOW
            elif command == "3":
                current_state = State.LISTS_SHOW
        elif current_state == State.TASKS_SHOW:
            print(f"Tasks of {task_lists[chosen_list].title}:")
            task_lists[chosen_list].tasks = get_tasks(task_list_id=task_lists[chosen_list].entity_id)
            tasks = task_lists[chosen_list].tasks

            string = "\n".join(
                [f'{i} -{" DONE" if task.done else ""} {task.description}' for i, task in enumerate(tasks)])
            print(string)
            command = input("Choose task (-1 add new, `back` for back): ")
            if command == "-1":
                task_decs = input("Name of new task description: ")
                create_task(task_decs, task_lists[chosen_list].entity_id)
            elif command == "back":
                current_state = State.LIST_OPTIONS
            elif command != "stop":
                current_state = State.TASK_OPTIONS
                chosen_task = int(command)
        elif current_state == State.TASK_OPTIONS:
            print(f"{tasks[chosen_task].description} options:"
                  "\n\t 1 - Mark task as done"
                  "\n\t 2 - Delete task"
                  "\n\t 3 - Back")
            command = input("Enter options: ")
            if command == "1":
                update_task(tasks[chosen_task].entity_id, done=True)
            elif command == "2":
                delete_task(tasks[chosen_task].entity_id)
                current_state = State.TASKS_SHOW
            elif command == "3":
                current_state = State.TASKS_SHOW
