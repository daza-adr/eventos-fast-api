from fastapi import FastAPI

from api.events.router import router as events_router
from api.users.router import router as users_router
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Events and Users API")

app.include_router(events_router)
app.include_router(users_router)
