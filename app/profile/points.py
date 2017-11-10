from ..models import Point, db


def get_total_point(user_id):
    points = Point.query.filter_by(user_id).group_by(user_id).all()
    return points.amount


def add_points(user_id, amount):
    point = Point(user=user_id, amount=amount)
    db.session.add(point)
    db.session.commit()
