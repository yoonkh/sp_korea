from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import PasswordField, StringField, SubmitField, DateTimeField, IntegerField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length, DataRequired, AnyOf

from .. import db
from ..models import Role, User


class ChangeUserEmailForm(FlaskForm):
    email = EmailField(
        'New email', validators=[InputRequired(), Length(1, 64), Email()])
    submit = SubmitField('Update email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class ChangeAccountTypeForm(FlaskForm):
    role = QuerySelectField(
        'New account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    submit = SubmitField('Update role')


class InviteUserForm(FlaskForm):
    role = QuerySelectField(
        'Account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    first_name = StringField(
        'First name', validators=[InputRequired(), Length(1, 64)])
    last_name = StringField(
        'Last name', validators=[InputRequired(), Length(1, 64)])
    email = EmailField(
        'Email', validators=[InputRequired(), Length(1, 64), Email()])
    submit = SubmitField('Invite')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class NewUserForm(InviteUserForm):
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(), EqualTo('password2', 'Passwords must match.')
        ])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])

    submit = SubmitField('Create')


class NewVideoForm(FlaskForm):
    name = StringField('이름', validators=[DataRequired(), Length(1, 128)])
    running_time_min = IntegerField('분')
    running_time_sec = IntegerField('초')
    price = IntegerField('가격')
    company = StringField('제공 업체', validators=[DataRequired(), Length(1, 32)])
    tags = StringField('태그', validators=[DataRequired()])
    link = StringField('링크', validators=[DataRequired()])
    description = TextAreaField('설명')
    submit = SubmitField('등록')

    def validate_running_time_sec(self, field):
        if int(field.data) >= 60:
            raise ValidationError('60초를 초과할수 없습니다.')

    def validate_running_time_min(self, field):
        if int(field.data) >= 60:
            raise ValidationError('60분을 초과할수 없습니다.')
