from datetime import datetime

from .. import db


class Point(db.Model):
    __tablename__ = 'points'
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User', backref='role', lazy='dynamic')
    amount = db.Column(db.Integer)
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
