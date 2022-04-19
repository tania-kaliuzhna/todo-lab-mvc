from typing import Optional, List

from dataclasses import dataclass, field

from model.base import BaseModel
from model.task import Task
from db import DbConnector
import config


@dataclass
class TaskList:
    title: str
    entity_id: Optional[int] = None
    tasks: List[Task] = field(default_factory=list)

    def save(self) -> None:
        if self.entity_id:
            props_list = [self.entity_id]
            DbConnector.update_entities(config.TASK_LIST_TABLE, {"id": self.entity_id}, {"title": self.title})
        else:
            DbConnector.create_entity(config.TASK_LIST_TABLE, self.title)
            self.entity_id = self.get(title=self.title)[0].entity_id

    @staticmethod
    def get(entity_id: Optional[int] = None, title: Optional[str] = None) -> list:
        entity_list = list(DbConnector.get_entities(config.TASK_LIST_TABLE, **{key: value for key, value in
                                                                               {"id": entity_id,
                                                                                "title": title}.items() if value}))
        return [TaskList(entity[1], entity[0], list(Task.get(task_list_id=entity[0])))
                for entity in entity_list]

    def delete(self) -> None:
        DbConnector.delete_entities(config.TASK_LIST_TABLE, id=self.entity_id)

    def add_and_save(self, task: Task):
        self.tasks.append(task)
        task.task_list_id = self.entity_id
        task.save()
