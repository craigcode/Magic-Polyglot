import datetime
from models import Task


def create_task(task_name: str, description: str, task_status: int, user_name: str):

    o = Task()
    mytype = type(o)
    task = mytype()

    ts = str(datetime.datetime.now())

    task.task_name = task_name
    task.description = description
    task.status = task_status
    task.seq_num = 0
    task.created_by = user_name
    task.created_date = ts
    task.updated_by = user_name
    task.updated_date = ts
    task.deleted = 0

    return task