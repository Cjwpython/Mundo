# coding: utf-8
import uuid


class TaskController():
    task_id = str(uuid.uuid4())
    base_url = ""

    @classmethod
    def set_task_id(cls, task_id: str):
        cls.task_id = task_id

    @classmethod
    def set_base_url(cls, base_url):
        cls.base_url = base_url
