from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField, TextAreaField, ValidationError, FloatField


class ExerciseForm(FlaskForm):
    name = StringField('운동명')
    laps = IntegerField('횟수')
    submit = SubmitField('저장하기')

    def validate_laps(self, field):
        if field.data <= 0:
            raise ValidationError('횟수가 0이거나 0보다 작을수 없습니다.')


class DietForm(FlaskForm):
    name = StringField('식사 종류')
    fullness = IntegerField('배부름 정도 (1~6)')
    submit = SubmitField('저장하기')

    def validate_fullness(self, field):
        if field.data <= 0 or field.data > 6:
            raise ValidationError('배부름 정도는 1에서 6사이로 적어주세요.')


class FavoriteListForm(FlaskForm):
    exercise = TextAreaField('운동 즐겨찾기')
    diet = TextAreaField('식단 즐겨찾기')
    submit = SubmitField('저장하기')


class WaterSleepForm(FlaskForm):
    water = FloatField('물')
    sleep = FloatField('수면')
    submit = SubmitField('저장하기')
