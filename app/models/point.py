from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from sqlalchemy.sql import label

from .. import db


class Point(db.Model):
    __tablename__ = 'points'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    amount = db.Column(db.Integer)
    datetime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @classmethod
    def add_points(cls, user_id, amount):
        point = Point(user=user_id, amount=amount)
        db.session.add(point)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    @classmethod
    def get_total_point(cls, user_id):
        user_info = db.session.query(Point.user_id, label('total_point', func.sum(Point.amount))).filter(
            Point.user_id == user_id).group_by(Point.user_id).first()
        return user_info.total_point

    @classmethod
    def get_points_list(cls, user_id):
        points = Point.query.filter_by(user_id=user_id).all()
        return points

    def __repr__(self):
        return '%s <Point \'%s\'>' % (self.user, self.amount)
