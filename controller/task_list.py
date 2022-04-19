from typing import List

from model.task_list import TaskList


def create_task_list(title) -> TaskList:
    task_list = TaskList(title)
    task_list.save()
    return task_list


def get_task_list(task_list_id: int) -> TaskList:
    task_list = TaskList.get(entity_id=task_list_id)[0]
    return task_list


def get_task_lists() -> List[TaskList]:
    task_lists = TaskList.get()
    return task_lists


def update_task_list(task_list_id: int, new_title: str) -> TaskList:
    task_list = TaskList.get(entity_id=task_list_id)[0]
    task_list.title = new_title
    task_list.save()
    return task_list


def delete_task_list(task_list_id: int) -> None:
    task_list = TaskList.get(entity_id=task_list_id)[0]
    task_list.delete()
