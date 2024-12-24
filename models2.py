from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Filter(db.Model):
    __tablename__ = 'filters'

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filter_size = db.Column(db.String(50), nullable=False)
    filter_type = db.Column(db.String(20), nullable=False)
    filter_count = db.Column(db.Integer, nullable=False)
    par = db.Column(db.Integer, nullable=False)
    storage = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.String(100), nullable=False)
    date_updated = db.Column(db.Date, nullable=True, default=date.today)
    pn = db.Column(db.String(30), nullable=True)

    def __init__(self, filter_size, filter_type, filter_count, par, storage, notes, pn):
        self.filter_size = filter_size
        self.filter_type = filter_type
        self.filter_count = filter_count
        self.par = par
        self.storage = storage
        self.notes = notes
        self.date_updated = date.today()
        self.pn = pn
