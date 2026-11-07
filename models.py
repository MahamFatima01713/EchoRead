from sqlalchemy import Column, DateTime, Integer, String, Text
from datetime import datetime

from database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=True)
    source_type = Column(String(50), nullable=False)
    source_url = Column(String(500), nullable=True)
    original_text = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    key_terms = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
