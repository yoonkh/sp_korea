from datetime import datetime

from app import db


class Diary(db.Model):
    __tablename__ = 'diarys'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    exercises = db.relationship('Exercise', backref='diary', lazy='dynamic')
    diets = db.relationship('Diet', backref='diary', lazy='dynamic')
    water_sleeps = db.relationship('WaterSleep', backref='diary', lazy='dynamic')

    def __repr__(self):
        return '<Diary \'%s\'>' % self.user.full_name()


class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32))  # 운동종류
    lap = db.Column(db.Integer())  # 횟수
    diary_id = db.Column(db.Integer, db.ForeignKey('diarys.id'))


class Diet(db.Model):
    __tablename__ = 'diets'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32))  # 식사종류
    fullness = db.Column(db.Integer, default=0)  # 배부름 정도
    diary_id = db.Column(db.Integer, db.ForeignKey('diarys.id'))


class WaterSleep(db.Model):
    __tablename__ = 'water_sleeps'
    id = db.Column(db.Integer, primary_key=True)
    water = db.Column(db.Float, default=0)
    sleep = db.Column(db.Float, default=0)
    diary_id = db.Column(db.Integer, db.ForeignKey('diarys.id'))

    def __repr__(self):
        return '<WaterSleep \'%s\' \'%s\'>' % self.water, self.sleep


class FavoriteList(db.Model):
    __tablename__ = 'favorite_lists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    exercise = db.Column(db.Text, default="팔굽혀펴기,턱걸이,크런치")
    diet = db.Column(db.Text, default="아침,점심,저녁,간식")


class Health(db.Model):
    __tablename__ = 'healths'
    id = db.Column(db.Integer, primary_key=True)
    blood_pressure_mmhg = db.Column(db.Integer())  # 혈압
    blood_suger_mddl = db.Column(db.Integer())  # 혈당
    mind_mg_dl = db.Column(db.Integer())  # 심리


class Etc(db.Model):
    __tablename__ = 'etcs'
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Integer())  # 체중
    fat = db.Column(db.Integer())  # 체지방
    skeletal_muscle = db.Column(db.Integer())  # 골격근
    smoke = db.Column(db.String(16))  # 흡연
    alcohol = db.Column(db.String(16))  # 음주
    bowel = db.Column(db.String(32))  # 배변


def get_diary_today(user):
    current_date = get_current_date_utc()
    diary = Diary.query.filter_by(user_id=user.id).filter(Diary.datetime >= current_date).first()
    if diary is None:
        diary = Diary(user_id=user.id)
        db.session.add(diary)
        db.session.commit()
    return diary


def get_current_date_utc():
    import datetime as d
    current_date = datetime.utcnow()
    if current_date.hour < 9:
        current_date -= d.timedelta(days=1)
    return current_date.replace(hour=9, minute=0, second=0, microsecond=0)
