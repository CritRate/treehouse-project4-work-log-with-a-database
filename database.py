import datetime

from peewee import *

db = SqliteDatabase('worklog.db')


class Entry(Model):
    name = CharField(max_length=30)
    date = DateField()
    time = IntegerField()
    task = TextField()
    notes = TextField()

    class Meta:
        database = db


def init_db():
    db.create_tables([Entry], safe=True)


def add_entry(*, name='', time=0, task='', notes='',
              date=datetime.datetime.today()):
    """
    Add entry to the database
    """
    entry = Entry.create(name=name, time=time, task=task,
                         notes=notes, date=date)
    return entry.save()


def edit_entry(id, **kwargs):
    """
    Edit already existing entry(date, time, task, notes)
    """
    entry = Entry.get_by_id(id)
    if 'date' in kwargs:
        entry.date = kwargs['date']
    if 'time' in kwargs:
        entry.time = kwargs['time']
    if 'task' in kwargs:
        entry.task = kwargs['task']
    if 'notes' in kwargs:
        entry.notes = kwargs['notes']
    return entry.save()


def delete_entry(id):
    """
    Delete entry
    """
    return Entry.delete_by_id(id)


def search_by_range(low_date, high_date):
    """
    Returns the selected records from date range
    """
    return Entry.select().where(Entry.date.between(low_date, high_date))


def search_by_time(time):
    return Entry.select().where(Entry.time == time)


def search_by_name(name):
    return Entry.select().where(Entry.name.contains(name))


def search_by_string(string):
    return Entry.select().where(Entry.task.contains(string)
                                | Entry.notes.contains(string))
