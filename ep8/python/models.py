from sqlmodel import Field, Session, SQLModel
from typing import Optional

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_name: str = Field(max_length=100)
    status: Optional[int] = Field(default=1)
    seq_num: Optional[int] = Field(default=0)
    description: str = Field(max_length=1000)
    created_by: Optional[str] = Field(max_length=30)
    created_date: Optional[str] = Field(max_length=19)
    updated_by: Optional[str] = Field(max_length=30)
    updated_date: Optional[str] = Field(max_length=19)
    deleted: Optional[int] = Field(default=0)