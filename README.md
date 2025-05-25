# 📚 Bookify - Plataforma de Libros y Audiolibros

Bookify es una aplicación web y móvil para explorar, leer y escuchar libros. Esta plataforma permite a los
administradores subir libros y audiolibros, y a los usuarios navegar y marcar sus libros favoritos.

---

## 🚀 Tecnologías Usadas

- **Backend:** FastAPI + SQLAlchemy
- **Base de Datos:** PostgreSQL
- **Frontend (Planeado):** Astro + Tailwind CSS
- **Autenticación:** JWT Tokens
- **ORM:** SQLAlchemy
- **Gestor de Entorno Virtual:** `venv`
- **Cargar Archivos:** `UploadFile` para audiolibros

---

## 📂 Estructura del Proyecto

```bash
bookify/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── role.py
│   │   ├── book.py
│   │   ├── favorite.py
│   │   ├── audiobook.py
│   │   └── review.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── role.py
│   │   ├── book.py
│   │   ├── favorite.py
│   │   ├── audiobook.py
│   │   ├── review.py
│   │   └── auth.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── role.py
│   │   ├── book.py
│   │   ├── favorite.py
│   │   ├── tts.py
│   │   ├── audiobook.py
│   │   ├── review.py
│   │   └── auth.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── security.py
│   ├── dependencies/
│   │    ├── __init__.py
│   │    └── auth.py
│   │
│   └──uploads/
│       ├── audio/
│       └── tts/
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Configuración Inicial

### 1. Clona el repositorio

```bash
git clone https://github.com/camiloCarabali/bookify-backend.git
cd bookify
```

### 2. Crea y activa un entorno virtual

```bash
# En Linux/Mac
python -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configura el archivo `.env`

Crea un archivo llamado .env en la raíz del proyecto con el siguiente contenido:

```bash
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/bookify
SECRET_KEY=clave_super_secreta
```

---

## ▶️ Ejecutar el Proyecto

```bash
uvicorn app.main:app --reload
```

Abre tu navegador en:

- 📎 http://localhost:8000/docs (Swagger UI)

---

## 🔁 Flujo de trabajo sugerido

### 1. Clona el repositorio y crea una rama desde `dev`:

```bash
git checkout develop
git pull
git checkout -b feature/mi-funcionalidad
```

### 2. Desarrolla y haz commits localmente:

```bash
git add .
git commit -m "✨ Agrega nueva funcionalidad"
```

### 3. Sube la rama al repositorio remoto:

```bash
git push origin feature/mi-funcionalidad
```

### 4. Crea un Pull Request hacia develop y espera revisión.

---

## 🧭 ¿Cuándo usar cada tipo de rama?

| Tipo de Rama | Cuándo Usarla                                                                  |
|--------------|--------------------------------------------------------------------------------|
| **prod**     | Solo para código listo para producción. Nunca se desarrolla directamente aquí. |
| **dev**      | Para integrar el trabajo de desarrollo antes de pasar a producción.            |
| **feature/** | Cuando estás construyendo una nueva funcionalidad o componente.                |
| **bugfix/**  | Cuando corriges errores detectados durante el desarrollo (en `dev`).           |
| **hotfix/**  | Cuando corriges errores críticos en producción (en `prod`).                    |
| **release/** | Cuando estás preparando una nueva versión estable para producción.             |

---

## ✅ Funcionalidades

- ✅ Registro y login de usuarios

- ✅ Roles de usuario (admin, user)

- ✅ Crear y listar libros

- ✅ Subir archivos de audiolibros

- ✅ Asociar audiolibros a libros

- ✅ Seguridad con JWT

- ✅ Acceso restringido a administradores

---

## 🗂 Próximos Pasos

- ⭐ Funcionalidad de favoritos

- 🤖 Texto a voz en tiempo real con IA

- 💻 Frontend con Astro y Tailwind

- 💬 Comentarios y calificaciones

---

## 📌 Recomendaciones

- Usa DBeaver para gestionar tu base de datos PostgreSQL

- Asegúrate de tener creada la carpeta uploads/audio

- Usa roles para controlar el acceso a los endpoints protegidos

- Protege tus claves secretas en el archivo .env

---

## 👨‍💻 Autor

Desarrollado con ❤️ por Camilo Carabali.