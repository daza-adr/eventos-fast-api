# API de eventos

API REST para crear, consultar, actualizar y eliminar eventos. Está construida
con FastAPI, SQLAlchemy y PostgreSQL.

## Requisitos

- Python 3.10 o posterior
- Una base de datos PostgreSQL

## Instalación en Windows

Desde la carpeta del proyecto, ejecuta:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Copia `.env.example` a `.env` y reemplaza `DATABASE_URL` con la URL de conexión
de tu base de datos. No publiques el archivo `.env`.

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

El cuerpo de creación y actualización debe incluir `name`, `description`,
`place` y `datetime` en formato ISO 8601.
