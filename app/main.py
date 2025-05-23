from fastapi import FastAPI
from .database import Base, engine
from .models import user, role
from .routers import user as user_router

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(user_router.router)


@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}
