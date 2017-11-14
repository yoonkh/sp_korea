from datetime import datetime

from flask_wtf.file import FileRequired, FileField
from wtforms import SelectField
from app import db

diary_users = db.Table('diary_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('diary_id', db.Integer, db.ForeignKey('diary.id')),
                       db.Column('food_id', db.Integer, db.ForeignKey('food.id')),
                       db.Column('water_id', db.Integer, db.ForeignKey('water.id')),
                       db.Column('sleep_id', db.Integer, db.ForeignKey('sleep.id')),
                       db.Column('health_id', db.Integer, db.ForeignKey('health.id')),
                       db.Column('etc_id', db.Integer, db.ForeignKey('etc.id')), )


class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(255))

    # 운동일지 다이어리

    # 운동 1,2,3,4
    exe_per_day = db.Column(db.String(10))
    # 운동종류 입력
    exe_per_day_type = db.Column(db.String(10))
    # 횟수 입력
    rep = db.Column(db.String(10))

    # 운동사진 업로드필드
    exe_photo = FileField(validators=[FileRequired()])

    # 운동이름 입력
    exe_name = db.Column(db.String(10))
    # 소모 칼로리 입력
    exe_kcal = db.Column(db.String(10))
    # 운동 시간 입력
    exe_time = db.Column(db.String(10))

    # gif 페이지 메모

    exe_memo = db.Column(db.String(255))

    # ... 기타 필드 추가

    create_dttm = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    users = db.relationship("User", secondary="diary_users", backref=db.backref('diarys'))


# 식단일지입니다

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # 식단 (음식) 종류
    breakfast_food_type = db.Column(db.String(10))
    lunch_food_type = db.Column(db.String(10))
    dinner_food_type = db.Column(db.String(10))
    snack_food_type = db.Column(db.String(10))
    etc_food_type = db.Column(db.String(10))

    # 식단 칼로리 입력
    kcal_food = db.Column(db.String(10))

    # 식단사진 업로드필드
    photo_food = FileField(validators=[FileRequired()])

    # 음식 이름 입력
    food_name = db.Column(db.String(10))

    # 음식 칼로리 입력
    food_kcal = db.Column(db.String(10))

    # 식사선택 select field
    food_select = SelectField('음식종류')

    # 음식 메모 입력란
    food_memo = db.Column(db.String(255))

    # ... 기타 필드 추가

    create_dttm = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    users = db.relationship("User", secondary="diary_users", backref=db.backref('foods'))


class Water(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 물 종류
    water_type = db.Column(db.String(10))
    # 물 이름 입력
    water_type_name = db.Column(db.String(10))
    # 물 용량 입력
    water_ml = db.Column(db.String(10))

    create_dttm = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    users = db.relationship("User", secondary="diary_users", backref=db.backref('waters'))


class Sleep(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # 수면시간 입력필드입니다
    sleep_time = db.Column(db.String(10))

    create_dttm = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    users = db.relationship("User", secondary="diary_users", backref=db.backref('sleeps'))


class Health(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # 혈압 - select field
    blood_pressure = SelectField('혈압')
    # 혈당 - select field
    blood_sugar = SelectField('혈당')
    # 심리 - select field
    mind = SelectField('심리')

    # 혈압 입력
    blood_pressure_mmhg = db.Column(db.String(10))
    # 혈당 입력
    blood_suger_mddl = db.Column(db.String(10))
    # 심리 입력
    mind_mg_dl = db.Column(db.String(10))

    create_dttm = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    users = db.relationship("User", secondary="diary_users", backref=db.backref('healths'))


class Etc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 체중 입력
    weight = db.Column(db.String(10))
    # 체지방 입력
    fat = db.Column(db.String(10))
    # 골격근 입력
    skeletal_muscle = db.Column(db.String(10))

    # 흡연 - select field
    smoke = SelectField('흡연')

    # 음주 - select field
    alcohol = SelectField('음주')

    # 배변 - select field
    bowel = SelectField('배변')

    create_dttm = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    user = db.relationship("User", secondary="diary_users", backref=db.backref('etcs'))
