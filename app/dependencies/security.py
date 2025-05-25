from fastapi import Depends, HTTPException, status, UploadFile, File
from app.models.user import User
from app.utils.security import decode_access_token


def get_current_user(token: str = Depends(decode_access_token)) -> User:
    user_email = token.get("sub")
    if not user_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_email


def get_current_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: se requiere rol de administrador"
        )
    return current_user


ALLOWED_AUDIO_TYPES = {"audio/mpeg", "audio/wav", "audio/ogg"}
MAX_FILE_SIZE = 100 * 1024 * 1024


def validate_audio_file(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(status_code=400, detail="Formato de audio no soportado")
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Archivo demasiado grande")
    return file
