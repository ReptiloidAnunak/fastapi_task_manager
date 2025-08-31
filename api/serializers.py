
from pydantic import BaseModel
from datetime import datetime
from typing import Union

class TaskSerializer(BaseModel):
    title: str
    description: str = "created"
    status: str = "pending"
    created_at:  Union[datetime, None] = None
    updated_at: Union[datetime, None] = None

    def __init__(self, **data):
        super().__init__(**data)
        
        if self.created_at is None:
            self.created_at = datetime.now()
        
        if self.updated_at is None:
            self.updated_at = datetime.now()

        
        