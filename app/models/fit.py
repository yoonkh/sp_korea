import datetime
from sqlalchemy.orm import backref, relationship

from app import db
from app.models import User
from app.models.diary import Diary


class Fit(db.Model):
    __tablename__ = 'fits'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    diary_id = db.Column(db.Integer, db.ForeignKey('diarys.id'))

    # ... 기타 필드 추가

    user = relationship(User, backref=backref("fits", cascade="all, delete-orphan"))
    diary = relationship(Diary, backref=backref("fits", cascade="all, delete-orphan"))
