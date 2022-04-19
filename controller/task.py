from typing import List

from model.task import Task


def create_task(desc: str, task_list_id: int, done: bool = False) -> Task:
    task = Task(desc, done, task_list_id=task_list_id)
    task.save()
    return task


def get_task(task_id: int) -> Task:
    task = Task.get(entity_id=task_id)[0]
    return task


def get_tasks(task_list_id: int) -> List[Task]:
    tasks = Task.get(task_list_id=task_list_id)
    return tasks


def update_task(task_id: int, **new_props) -> Task:
    task = Task.get(entity_id=task_id)[0]
    for key, value in new_props.items():
        if hasattr(task, key):
            setattr(task, key, value)
    task.save()
    return task


def delete_task(task_id: int) -> None:
    task = Task.get(entity_id=task_id)[0]
    task.delete()
