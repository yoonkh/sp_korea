from datetime import datetime

from app import db


class Survey(db.Model):
    __tablename__ = 'surveys'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    code = db.Column(db.String)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
