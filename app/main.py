from fastapi import FastAPI
from app.routers import auth, user, book, audiobook, favorite, categories, review, tts
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.dependencies.limiter import limiter
from dotenv import load_dotenv
from app.models.role import Role
from app.models.user import User
from app.models.book import Book
from app.models.audiobook import Audiobook
from app.models.category import Category
from app.models.favorite import Favorite
from app.models.review import Review
import os

app = FastAPI()
app.state.limiter = limiter

load_dotenv()

try:
    Base.metadata.create_all(bind=engine)
    print("[INFO] Tablas creadas correctamente")
except Exception as e:
    raise RuntimeError(f"[ERROR] No se pudieron crear las tablas: {e}")

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE"]
ALLOWED_HEADERS = ["Content-Type", "Authorization"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
    allow_credentials=True,
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(book.router)
app.include_router(audiobook.router)
app.include_router(favorite.router)
app.include_router(categories.router)
app.include_router(review.router)
app.include_router(tts.router)


@app.get("/")
def read_root():
    return {"message": "API funcionando"}
