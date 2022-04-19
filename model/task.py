from typing import Optional

from dataclasses import dataclass

from model.base import BaseModel
from db import DbConnector
import config


@dataclass
class Task(BaseModel):
    description: str
    done: bool = False
    entity_id: Optional[int] = None
    task_list_id: Optional[int] = None

    def save(self) -> None:
        if self.entity_id:
            DbConnector.update_entities(config.TASK_TABLE,
                                        {"id": self.entity_id},
                                        {"description": self.description,
                                         "done": self.done,
                                         f"{config.TASK_LIST_TABLE}_id": self.task_list_id})
        else:
            DbConnector.create_entity(config.TASK_TABLE, self.description, self.done, self.task_list_id)
            self.entity_id = self.get(**{"description": self.description,
                                         "done": self.done,
                                         f"task_list_id": self.task_list_id})[0].entity_id

    @staticmethod
    def get(entity_id: Optional[int] = None,
            description: Optional[str] = None,
            done: Optional[bool] = None,
            task_list_id: Optional[int] = None
            ) -> list:
        entity_list = list(DbConnector.get_entities(config.TASK_TABLE,
                                                    **{key: value for key, value in
                                                       {"id": entity_id,
                                                        "description": description,
                                                        "done": done,
                                                        f"{config.TASK_LIST_TABLE}_id": task_list_id}.items() if
                                                       value}))
        return [Task(entity[1], entity[2], entity[0], entity[3]) for entity in entity_list]

    def delete(self) -> None:
        DbConnector.delete_entities(config.TASK_TABLE, id=self.entity_id)
