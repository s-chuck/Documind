from fastapi import FastAPI
from app.api.documents import router as documents_router
from app.api.auth import router as authentication_router
from app.models.user import User
from app.database import Base, engine
from app.api.chat import router as chat_router
Base.metadata.create_all(engine)

app = FastAPI(title="DocuMind API")


#root router
@app.get("/")
async def root():
    return {"message": "Welcome to our website"}

#auth router
#chat router
#documents router
#conversation router
#feedback router
app.include_router(authentication_router)
app.include_router(documents_router)
app.include_router(chat_router)