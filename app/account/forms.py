from flask import url_for
from flask_wtf import Form
from wtforms import ValidationError
from wtforms.fields import (BooleanField, PasswordField, StringField,
                            SubmitField)
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length

from ..models import User


class LoginForm(Form):
    email = EmailField(
        '이메일', validators=[InputRequired(), Length(1, 64), Email()])
    password = PasswordField('비밀번호', validators=[InputRequired()])
    remember_me = BooleanField('계정기억하기', default=True)
    submit = SubmitField('로그인')


class RegistrationForm(Form):
    first_name = StringField(
        '이름', validators=[InputRequired(), Length(1, 64)])
    last_name = StringField(
        '성', validators=[InputRequired(), Length(1, 64)])
    email = EmailField(
        '이메일', validators=[InputRequired(), Length(1, 64), Email()])
    password = PasswordField(
        '비밀번호',
        validators=[
            InputRequired(), EqualTo('password2', '두 비밀번호가 같아야합니다.')
        ])
    password2 = PasswordField('비밀번호 확인', validators=[InputRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('이메일이 이미 등록되었습니다. ('
                                  '<a href="{}">로그인</a>을 시도하셨었나요?)'
                                  .format(url_for('account.login')))


class RequestResetPasswordForm(Form):
    email = EmailField(
        '이메일', validators=[InputRequired(), Length(1, 64), Email()])
    submit = SubmitField('확인')

    # We don't validate the email address so we don't confirm to attackers
    # that an account with the given email exists.


class ResetPasswordForm(Form):
    email = EmailField(
        'Email', validators=[InputRequired(), Length(1, 64), Email()])
    new_password = PasswordField(
        '새 비밀번호',
        validators=[
            InputRequired(), EqualTo('new_password2', '두 비밀번호가 같아야합니다.')
        ])
    new_password2 = PasswordField(
        '새 비밀번호 확인', validators=[InputRequired()])
    submit = SubmitField('비밀번호 갱신')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('알수없는 이메일 주소.')


class CreatePasswordForm(Form):
    password = PasswordField(
        '비밀번호',
        validators=[
            InputRequired(), EqualTo('password2', '두 비밀번호가 같아야합니다..')
        ])
    password2 = PasswordField(
        '새 비밀번호 확인', validators=[InputRequired()])
    submit = SubmitField('비밀번호 설정')


class ChangePasswordForm(Form):
    old_password = PasswordField('이전 비밀번호', validators=[InputRequired()])
    new_password = PasswordField(
        '새 비밀번호',
        validators=[
            InputRequired(), EqualTo('new_password2', 'Passwords must match.')
        ])
    new_password2 = PasswordField(
        '새 비밀번호 확인', validators=[InputRequired()])
    submit = SubmitField('비밀번호 갱신')


class ChangeEmailForm(Form):
    email = EmailField(
        '새 이메일', validators=[InputRequired(), Length(1, 64), Email()])
    password = PasswordField('비밀번호 갱신', validators=[InputRequired()])
    submit = SubmitField('비밀번호 업데이트')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('이미 등록된 이메일 입니다.')
