from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Events
from schemas import EventCreate, EventResponse

# Crear la tabla en Neon si todavía no existe
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Events API")


# ====================================
# GET: Consultar todos los eventos          
# ====================================
@app.get("/events", response_model=list[EventResponse])
def get_events(db: Session = Depends(get_db)):
    events = db.query(Events).all()
    return events   


# ====================================
# GET: Consultar un evento  
# ====================================
@app.get("/events/{event_id}", response_model=EventResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    event = db.query(Events).filter(
        Events.id == event_id
    ).first()

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event


# ====================================
# POST: Registrar un evento
# ====================================
@app.post("/events", response_model=EventResponse, status_code=201)
def create_event(
    data: EventCreate,
    db: Session = Depends(get_db)
):
    # Validar que el nombre del evento no esté registrado
    existing = db.query(Events).filter(
        Events.name == data.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Event name already registered"
        )

    event = Events(
        name=data.name,
        description=data.description,
        place=data.place,
        datetime=data.datetime
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


# ====================================
# PUT: Actualizar un evento
# ====================================
@app.put("/events/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    data: EventCreate,
    db: Session = Depends(get_db)
):
    event = db.query(Events).filter(
        Events.id == event_id
    ).first()

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    # Validar que el nombre del evento no esté registrado
    duplicated = db.query(Events).filter(
        Events.name == data.name,
        Events.id != event_id
    ).first()

    if duplicated:
        raise HTTPException(
            status_code=400,
            detail="Event name already registered"
        )

    event.name = data.name
    event.description = data.description
    event.place = data.place
    event.datetime = data.datetime

    db.commit()
    db.refresh(event)

    return event


# ====================================
# DELETE: Eliminar un evento
# ====================================
@app.delete("/events/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    event = db.query(Events).filter(
        Events.id == event_id
    ).first()

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    db.delete(event)
    db.commit()

    return {
        "message": "Event deleted successfully"
    }