import datetime

from flask_sqlalchemy import Model
from sqlalchemy.orm import relationship

from app import db
from app.models import Role




diary_users = db.Table('diary_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('diary_id', db.Integer, db.ForeignKey('diary.id')),
                       db.Column('food_id', db.Integer, db.ForeignKey('food.id'))
                       )


create_dttm = db.Column(db.DateTime.Date, nullable=False)


users = db.relationship("User", secondary="diary_users", backref=db.backref('diarys',
                                                                            'foods',
                                                                            'waters',
                                                                            ))


class Diary(db.Model, create_dttm, users):

    id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(255))

    # 운동일지 다이어리
    exe_per_day = db.Column(db.String(10))

    exe_per_day_type = db.Column(db.String(10))

    rep = db.Column(db.String(10))

    # 운동사진 업로드필드
    # exe_photo = db.Column(db.)
    exe_name = db.Column(db.String(10))
    exe_kcal = db.Column(db.String(10))
    exe_time = db.Column(db.String(10))


    # gif 페이지 메모
    exe_memo = db.Column(db.String(255))

    # ... 기타 필드 추가


    # create_dttm = db.Column(db.DateTime.Date, nullable=False)

    # users = db.relationship("User", secondary="diary_users", backref=db.backref('diarys'))





# 식단일지입니다
class Food(db.Model, create_dttm, users):

    id = db.Column(db.Integer, primary_key=True)
    breakfast_food_type = db.Column(db.String(10))
    lunch_food_type = db.Column(db.String(10))
    dinner_food_type = db.Column(db.String(10))
    snack_food_type = db.Column(db.String(10))
    etc_food_type = db.Column(db.String(10))
    kcal_food = db.Column(db.String(10))

    # 식단사진 업로드필드
    # photo_food = db.Column(db.)

    food_name = db.Column(db.String(10))
    food_kcal = db.Column(db.String(10))

    # 식사선택 select field
    # food_select = db.

    food_memo = db.Column(db.String(255))


    # ... 기타 필드 추가

    # create_dttm = db.Column(db.DateTime.Date, nullable=False)

    # users = db.relationship("User", secondary="diary_users", backref=db.backref('foods'))



class Water(db.Model, create_dttm, users):
    id = db.Column(db.Integer, primary_Key=True)

    water_type = db.Column(db.String(10))

    water_type_name = db.Column(db.String(10))

    water_ml = db.Column(db.String(10))

    # users = db.relationship("User", secondary="diary_users", backref=db.backref('waters'))







