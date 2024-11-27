from pydantic import BaseModel

class KnowledgeBaseBase(BaseModel):
    title: str
    content: str

class KnowledgeBaseCreate(KnowledgeBaseBase):
    pass

class KnowledgeBase(KnowledgeBaseBase):
    id: int

    class Config:
        from_attributes = True