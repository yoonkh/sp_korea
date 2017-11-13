from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, IntegerField, StringField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import InputRequired


class DiaryForm(FlaskForm):
    number = IntegerField('운동횟수 1')
    type = StringField('운동종류 당구')
    photo = FileField('사진 업로드')
    submit = SubmitField('저장하기')


class UploadForm(FlaskForm):
    file = FileField('이미지', render_kw={'multiple': True})


class DiaryFormPhoto(FlaskForm):
    name = StringField('운동이름')
    kcal = IntegerField('소모 칼로리 kcal')
    time = IntegerField('Min or hour')
    submit = SubmitField('저장하기')


class FitForm(FlaskForm):
    memo = StringField('오늘 피드백 받은 내용 메모')


class FoodForm(FlaskForm):
    food_type = StringField('음식 종류')
    kcal = IntegerField('칼로리')
    submit = SubmitField('저장')


class FoodFormPhoto(FlaskForm):
    food_photo = FileField('사진 업로드')

    food_name = StringField('음식이름')
    eat = SelectField(label='식사', choices=[('', '아침'),
                                           ('', '점심'),
                                           ('', '저녁'),
                                           ('', '간식')])

    kcal = IntegerField('칼로리')
    memo = StringField('메모')
    submit = SubmitField('저장')


class WaterForm(FlaskForm):
    water_type = StringField('물 종류')
    water_size = IntegerField('물 용량 (ml)')
    submit = SubmitField('저장')


class SleepForm(FlaskForm):
    sleep = IntegerField('수면시간 0 ~ 12시간')
    submit = SubmitField('저장')


class HealthForm(FlaskForm):
    pressure = StringField('mmHg')
    sugar = StringField('mg/dl')
    mind = StringField('mg/dl')
    submit = SubmitField('저장')


class EtcForm(FlaskForm):
    kg = IntegerField('체중 kg')
    fat = IntegerField('체지방량 kg or %')
    bone = IntegerField('골격근량 kg')
    smoke = SelectField(label='흡연', choices=[('', '0갑'),
                                             ('', '1/2갑'),
                                             ('', '1갑'),
                                             ('', '2갑이상')])

    alcohol = SelectField(label='음주', choices=[('', '0병'),
                                               ('', '1/2병'),
                                               ('', '1병'),
                                               ('', '2병이상')])

    bowel = SelectField(label='배변', choices=[('', '못함'),
                                             ('', '설사'),
                                             ('', '쾌변')])
    submit = SubmitField('저장하기')


class MyquestionForm(FlaskForm):
    submit = SubmitField('저장')


class MyreviewForm(FlaskForm):
    review = SelectField(label='태그', choices=[('', '신체정보'),
                                              ('', '관절기능'),
                                              ('', '기초체력'),
                                              ('', '체형분석'),
                                              ('', '1RM'),
                                              ('', 'VO2max')])
    submit = SubmitField('저장')


class VideoForm(FlaskForm):
    submit = SubmitField('올리기')


class TagForm(FlaskForm):
    search = StringField('검색창')


