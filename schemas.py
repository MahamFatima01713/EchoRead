from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# 1. Data the user sends when adding a document by article link
class DocumentFromURL(BaseModel):
    url: str
    title: Optional[str] = None


# 2. Data the user sends when adding a document by pasting text
class DocumentFromText(BaseModel):
    text: str
    title: Optional[str] = None


# 3. Data our API sends back when someone asks for a document
class DocumentOut(BaseModel):
    id: int
    title: Optional[str] = None
    source_type: str
    source_url: Optional[str] = None
    original_text: str
    summary: Optional[str] = None
    key_terms: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
