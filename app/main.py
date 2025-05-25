from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import user, auth, book, audiobook, favorite, tts, review, categories

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(book.router)
app.include_router(audiobook.router)
app.include_router(favorite.router)
app.include_router(tts.router)
app.include_router(review.router)
app.include_router(categories.router)


@app.get("/")
def read_root():
    return {"message": "API funcionando"}
