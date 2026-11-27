from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.events.models import Events
from api.events.schemas import EventCreate, EventResponse
from database import get_db

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[EventResponse])
def get_events(db: Session = Depends(get_db)):
    return db.query(Events).all()


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Events).filter(Events.id == event_id).first()

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return event


@router.post("", response_model=EventResponse, status_code=201)
def create_event(data: EventCreate, db: Session = Depends(get_db)):
    existing = db.query(Events).filter(Events.name == data.name).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Event name already registered",
        )

    event = Events(
        name=data.name,
        description=data.description,
        place=data.place,
        datetime=data.datetime,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    data: EventCreate,
    db: Session = Depends(get_db),
):
    event = db.query(Events).filter(Events.id == event_id).first()

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    duplicated = db.query(Events).filter(
        Events.name == data.name,
        Events.id != event_id,
    ).first()

    if duplicated:
        raise HTTPException(
            status_code=400,
            detail="Event name already registered",
        )

    event.name = data.name
    event.description = data.description
    event.place = data.place
    event.datetime = data.datetime

    db.commit()
    db.refresh(event)

    return event


@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Events).filter(Events.id == event_id).first()

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(event)
    db.commit()

    return {"message": "Event deleted successfully"}
