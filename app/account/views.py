from flask import flash, redirect, render_template, request, url_for, current_app, jsonify
from flask_login import (current_user, login_required, login_user,
                         logout_user)
from flask_rq import get_queue
from iamport import Iamport
from sqlalchemy import desc

from ..survey.pattern import find_pattern
from ..models.survey import Survey
from . import account
from .. import db
from ..email import send_email
from ..models import User, Point
from .forms import (ChangeEmailForm, ChangePasswordForm, CreatePasswordForm,
                    LoginForm, RegistrationForm, RequestResetPasswordForm,
                    ResetPasswordForm)


@account.route('/login', methods=['GET', 'POST'])
def login():
    """Log in an existing user."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password_hash is not None and \
                user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('로그인 되었습니다. Welcome back!', 'success')
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('알수 없는 이메일이나 비밀번호 입니다.', 'form-error')
    return render_template('account/login.html', form=form)


@account.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user, and send them a confirmation email."""
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        confirm_link = url_for('account.confirm', token=token, _external=True)
        get_queue().enqueue(
            send_email,
            recipient=user.email,
            subject='Confirm Your Account',
            template='account/email/confirm',
            user=user,
            confirm_link=confirm_link)
        flash('확인 이메일이 {}로 보내졌습니다.'.format(user.email),
              'warning')
        return redirect(url_for('main.index'))
    return render_template('account/register.html', form=form)


@account.route('/logout')
@login_required
def logout():
    logout_user()
    flash('로그아웃되셨습니다.', 'info')
    return redirect(url_for('main.index'))


@account.route('/manage', methods=['GET', 'POST'])
@account.route('/manage/info', methods=['GET', 'POST'])
@login_required
def manage():
    """Display a user's account information."""
    survey = Survey.query.filter_by(user_id=current_user.id).order_by(desc(Survey.datetime)).first()
    if survey is not None:
        result = find_pattern(survey.code)
    else:
        result = '설문조사를 진행해주세요.'
    return render_template('account/manage.html', user=current_user, form=None, result=result)


@account.route('/manage/point')
@login_required
def manage_point():
    """포인트 충전 및 관리 화면."""
    return render_template('account/manage.html', user=current_user, form=None)


# 아임포트에서 결제를 재확인해야하는 부분이 생략됨. 추후 추가 필요
@account.route('/manage/payment', methods=['GET', 'POST'])
def manage_payment():
    iamport_api = Iamport(imp_key=current_app.config['IMP_KEY'], imp_secret=current_app.config['IMP_SECRET'])
    # result = iamport_api.is_paid(request.args.get('amount', 0), imp_uid=request.args.get('imp_uid', None))
    point = Point(user_id=current_user.id, amount=request.args.get('amount', 10000))
    db.session.add(point)
    db.session.commit()
    return jsonify({'data': render_template('account/email/success_form.html', code=302)})
    # return jsonify({'data': render_template('account/email/fail_form.html', code=404)})


@account.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    """Respond to existing user's request to reset their password."""
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_password_reset_token()
            reset_link = url_for(
                'account.reset_password', token=token, _external=True)
            get_queue().enqueue(
                send_email,
                recipient=user.email,
                subject='Reset Your Password',
                template='account/email/reset_password',
                user=user,
                reset_link=reset_link,
                next=request.args.get('next'))
        flash('비밀번호 갱신 링크가 {}로 보내졌습니다.'
              .format(form.email.data), 'warning')
        return redirect(url_for('account.login'))
    return render_template('account/reset_password.html', form=form)


@account.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset an existing user's password."""
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('존재하지 않는 이메일입니다.', 'form-error')
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.new_password.data):
            flash('비밀번호가 업데이트 되었습니.', 'form-success')
            return redirect(url_for('account.login'))
        else:
            flash('해당 링크의 기한이 지났습니다, 다시 시도하여 주십시오.',
                  'form-error')
            return redirect(url_for('main.index'))
    return render_template('account/reset_password.html', form=form)


@account.route('/manage/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change an existing user's password."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash('비밀번호가 갱신되었습니다.', 'form-success')
            return redirect(url_for('main.index'))
        else:
            flash('원 비밀번호가 정확하지 않습니다.', 'form-error')
    return render_template('account/manage.html', form=form)


@account.route('/manage/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    """Respond to existing user's request to change their email."""
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            change_email_link = url_for(
                'account.change_email', token=token, _external=True)
            get_queue().enqueue(
                send_email,
                recipient=new_email,
                subject='Confirm Your New Email',
                template='account/email/change_email',
                # current_user is a LocalProxy, we want the underlying user
                # object
                user=current_user._get_current_object(),
                change_email_link=change_email_link)
            flash('확인메일이 {}로 전송되었습니다.'.format(new_email),
                  'warning')
            return redirect(url_for('main.index'))
        else:
            flash('알수 없는 이메일이나 비밀번호입니다.', 'form-error')
    return render_template('account/manage.html', form=form)


@account.route('/manage/change-email/<token>', methods=['GET', 'POST'])
@login_required
def change_email(token):
    """Change existing user's email with provided token."""
    if current_user.change_email(token):
        flash('이메일 주소가 갱신되었습니다.', 'success')
    else:
        flash('해당 링크의 기한이 지났습니다 다시 시도하여 주십시오.', 'error')
    return redirect(url_for('main.index'))


@account.route('/confirm-account')
@login_required
def confirm_request():
    """Respond to new user's request to confirm their account."""
    token = current_user.generate_confirmation_token()
    confirm_link = url_for('account.confirm', token=token, _external=True)
    get_queue().enqueue(
        send_email,
        recipient=current_user.email,
        subject='Confirm Your Account',
        template='account/email/confirm',
        # current_user is a LocalProxy, we want the underlying user object
        user=current_user._get_current_object(),
        confirm_link=confirm_link)
    flash('새로운 확인 메일이 {}로 전송되었습니다.'.format(
        current_user.email), 'warning')
    return redirect(url_for('main.index'))


@account.route('/confirm-account/<token>')
@login_required
def confirm(token):
    """Confirm new user's account with provided token."""
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm_account(token):
        flash('계정이 확인되었습니다.', 'success')
    else:
        flash('해당 링크의 기한이 지났거나 확인할수 없습니다 다시 시도하여 주십시오.', 'error')
    return redirect(url_for('main.index'))


@account.route(
    '/join-from-invite/<int:user_id>/<token>', methods=['GET', 'POST'])
def join_from_invite(user_id, token):
    """
    Confirm new user's account with provided token and prompt them to set
    a password.
    """
    if current_user is not None and current_user.is_authenticated:
        flash('이미 로그인 되어있습니다.', 'error')
        return redirect(url_for('main.index'))

    new_user = User.query.get(user_id)
    if new_user is None:
        return redirect(404)

    if new_user.password_hash is not None:
        flash('이미 회원가입이 되어있습니다.', 'error')
        return redirect(url_for('main.index'))

    if new_user.confirm_account(token):
        form = CreatePasswordForm()
        if form.validate_on_submit():
            new_user.password = form.password.data
            db.session.add(new_user)
            db.session.commit()
            flash('비밀번호가 설정되었습니다. 마이페이지에서 계정 설정을 확인하시고 수정하실수 있습니다.', 'success')
            return redirect(url_for('account.login'))
        return render_template('account/join_invite.html', form=form)
    else:
        flash('해당 링크는 존재하지 않거나 기한이 지났습니다.'
              '새로운 확인 메일을 전송하였습니다.', 'error')
        token = new_user.generate_confirmation_token()
        invite_link = url_for(
            'account.join_from_invite',
            user_id=user_id,
            token=token,
            _external=True)
        get_queue().enqueue(
            send_email,
            recipient=new_user.email,
            subject='You Are Invited To Join',
            template='account/email/invite',
            user=new_user,
            invite_link=invite_link)
    return redirect(url_for('main.index'))


@account.before_app_request
def before_request():
    """Force user to confirm email before accessing login-required routes."""
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:8] != 'account.' \
            and request.endpoint != 'static':
        return redirect(url_for('account.unconfirmed'))


@account.route('/unconfirmed')
def unconfirmed():
    """Catch users with unconfirmed emails."""
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('account/unconfirmed.html')
