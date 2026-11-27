# API de eventos y usuarios

API REST construida con FastAPI, SQLAlchemy y PostgreSQL. Incluye CRUD para
eventos y usuarios. Las contraseñas de usuarios se guardan como hashes y no se
incluyen en las respuestas.

## Estructura

```text
api/
  events/
    models.py
    router.py
    schemas.py
  users/
    models.py
    schemas.py
main.py
database.py
```

Las rutas de usuarios y el hash de contraseñas están definidos en `main.py`.

## Requisitos

- Python 3.10 o posterior
- Una base de datos PostgreSQL

## Instalación en Windows

Desde la carpeta del proyecto, ejecuta:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt
```

## Ejecutar

```powershell
python -m uvicorn main:app --reload
```

La documentación interactiva estará en <http://127.0.0.1:8000/docs>.

## Rutas

- `GET /events`: listar eventos.
- `GET /events/{event_id}`: consultar un evento.
- `POST /events`: crear un evento.
- `PUT /events/{event_id}`: actualizar un evento.
- `DELETE /events/{event_id}`: eliminar un evento.
- `GET /users`: listar usuarios.
- `GET /users/{user_id}`: consultar un usuario.
- `POST /users`: crear un usuario.
- `PUT /users/{user_id}`: actualizar un usuario.
- `DELETE /users/{user_id}`: eliminar un usuario.

El cuerpo de creación y actualización debe incluir `name`, `description`,
`place` y `datetime` en formato ISO 8601.

El cuerpo de creación y actualización de usuarios debe incluir `nombre`,
`correo` y `contraseña`. La contraseña debe tener entre 8 y 128 caracteres; el
correo debe ser válido y único.
