import datetime

from sqlalchemy.orm import relationship

from app import db
from app.models import Role


class Diary(db.Model):
    __tablename__ = 'diarys'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))

    # ... 기타 필드 추가

    users = relationship("User", secondary="fits")
