from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from .database import Base, engine
import uuid
class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, unique=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="created")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, nullable=True)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not hasattr(self, 'id') or self.id is None:
            self.id = str(uuid.uuid4())

def init_db():
    Base.metadata.create_all(bind=engine)