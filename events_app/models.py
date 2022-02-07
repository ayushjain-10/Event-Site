"""Create database models to represent tables."""
from events_app import db
from sqlalchemy.orm import backref
import enum


class Type(enum.Enum):
    Party = 1
    Study = 2
    Networking = 3
    ALL = 4

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80))
    phone = db.Column(db.Integer)
    events_attending = db.relationship(
        "Event", secondary="guest_event", back_populates="guests"
    )

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(140))
    date_and_time = db.Column(db.DateTime)
    event_type = db.Column(db.Enum(Type), default=Type.ALL)
    guests = db.relationship(
        "Guest", secondary="guest_event", back_populates="events_attending"
    )

guest_event_table = db.Table(
    "guest_event",
    db.Column("guest_id", db.Integer, db.ForeignKey("guest.id")),
    db.Column("event_id", db.Integer, db.ForeignKey("event.id")),
)
