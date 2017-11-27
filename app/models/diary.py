from datetime import datetime

from app import db


class Diary(db.Model):
    __tablename__ = 'diarys'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    exercises = db.relationship('Exercise', backref='diary', lazy='dynamic')
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'))
    water_id = db.Column(db.Integer, db.ForeignKey('waters.id'))
    sleep_id = db.Column(db.Integer, db.ForeignKey('sleeps.id'))
    health_id = db.Column(db.Integer, db.ForeignKey('healths.id'))
    etc_id = db.Column(db.Integer, db.ForeignKey('etcs.id'))


def get_diary_today(user):
    current_date = get_current_date_utc()
    diary = Diary.query.filter(Diary.datetime >= current_date).filter_by(user_id=user.id).first()
    if diary is None:
        diary = Diary(user_id=user.id)
    return diary


def get_current_date_utc():
    import datetime as d
    current_date = datetime.utcnow()
    if current_date.hour < 9:
        current_date -= d.timedelta(days=1)
    current_date.replace(hour=9, minute=0, second=0, microsecond=0)
    return current_date


class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32))  # 운동종류
    lap = db.Column(db.Integer())  # 횟수
    diary_id = db.Column(db.Integer, db.ForeignKey('diarys.id'))


class FavoriteExercise(db.Model):
    __tablename__ = 'favorite_exercises'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.Text, default="팔굽혀펴기,턱걸이,크런치")


class Food(db.Model):
    __tablename__ = 'foods'
    id = db.Column(db.Integer, primary_key=True)
    fullness = db.Column(db.Integer, default=0)  # 배부름 정도
    diary_id = db.relationship('Diary', backref='food', lazy='dynamic')


class Water(db.Model):
    __tablename__ = 'waters'
    id = db.Column(db.Integer, primary_key=True)
    cup = db.Column(db.Integer, default=0)
    diary_id = db.relationship('Diary', backref='water', lazy='dynamic')


class Sleep(db.Model):
    __tablename__ = 'sleeps'
    id = db.Column(db.Integer, primary_key=True)
    sleep_time = db.Column(db.Integer)  # 수면시간
    diary_id = db.relationship('Diary', backref='sleep', lazy='dynamic')


class Health(db.Model):
    __tablename__ = 'healths'
    id = db.Column(db.Integer, primary_key=True)
    blood_pressure_mmhg = db.Column(db.Integer())  # 혈압
    blood_suger_mddl = db.Column(db.Integer())  # 혈당
    mind_mg_dl = db.Column(db.Integer())  # 심리
    diary_id = db.relationship('Diary', backref='health', lazy='dynamic')


class Etc(db.Model):
    __tablename__ = 'etcs'
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Integer())  # 체중
    fat = db.Column(db.Integer())  # 체지방
    skeletal_muscle = db.Column(db.Integer())  # 골격근
    smoke = db.Column(db.String(16))  # 흡연
    alcohol = db.Column(db.String(16))  # 음주
    bowel = db.Column(db.String(32))  # 배변
    diary_id = db.relationship('Diary', backref='etc', lazy='dynamic')
