"""Import packages and modules."""
import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from events_app.models import Event, Guest

# Import app and db from events_app package so that we can run app
from events_app import app, db

main = Blueprint('main', __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def index():
    """Show upcoming events to users!"""

    events = ""
    try:
        events = Event.query.all()

    except:
        print("No event for now")
    for event in events:
        print(type(event.date_and_time))
    return render_template("index.html", events=events)


@main.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new event."""
    if request.method == 'POST':
        new_event_title = request.form.get('title')
        new_event_description = request.form.get('description')
        date = request.form.get('date')
        time = request.form.get('time')

        try:
            date_and_time = datetime.strptime(
                f'{date} {time}',
                '%Y-%m-%d %H:%M')
        except ValueError:
            return render_template('create.html', 
                error='Incorrect datetime format! Please try again.')

        new_event = Event(
            title=new_event_title,
            description=new_event_description,
            date_and_time=date_and_time,
        )
        db.session.add(new_event)
        db.session.commit()

        flash('Event created.')
        return redirect(url_for('main.index'))
    else:
        return render_template('create.html')

@main.route('/event/<event_id>', defaults={'error': None})
@main.route('/event/<event_id>/<error>', methods=['GET'])
def event_detail(event_id, error=""):
    """Show a single event."""
    event = ""
    try:
        event = Event.query.filter_by(id=event_id).one()
    except:
        print("No event was found")
    return render_template('event_detail.html', event=event, guests=event.guests, error=error)

@main.route('/event/<event_id>', defaults={'error': None}, methods=['POST'])
@main.route('/event/<event_id>/<error>', methods=['POST'])
def rsvp(event_id,error=""):
    """RSVP to an event."""

    is_returning_guest = request.form.get('returning')
    guest_name = request.form.get('guest_name')
    event = Event.query.filter_by(id=event_id).one()
    guest = ""

    if is_returning_guest:

        try:
            guest = Guest.query.filter_by(name=guest_name).one()
        except:
            
            return redirect(url_for("main.event_detail", event_id=event_id, error="You are not returning Guest! Please register first."))

    else:
        guest_email = request.form.get('email')
        guest_phone = request.form.get('phone')
        guest = Guest(name=guest_name, email=guest_email, phone=guest_phone)

    guest.events_attending.append(event)
    db.session.add(guest)
    db.session.commit()

    flash("Success! Please click")
    return redirect(url_for("main.event_detail", event_id=event_id))


@main.route('/guest/<guest_id>')
def guest_detail(guest_id):
    guest = ""
    try:
        guest = Guest.query.filter_by(id=guest_id).one()
    except:
        print("No guests were found")
    return render_template("guest_detail.html", guest=guest, events_attending=guest.events_attending)
