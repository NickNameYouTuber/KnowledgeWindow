import os
import sys
from imp import reload

# Установка кодировки по умолчанию
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

from fastapi import FastAPI
from app.routes import auth_routes, knowledge_base_routes

app = FastAPI()

app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(knowledge_base_routes.router, prefix="/knowledge-base", tags=["knowledge-base"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Knowledge Base API"}