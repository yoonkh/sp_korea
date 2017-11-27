from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from sqlalchemy import desc

from app import db
from ..models import get_diary_today, Exercise, FavoriteList, Diet, WaterSleep, Diary
from .forms import ExerciseForm, FavoriteListForm, DietForm, WaterSleepForm
from . import diary


@diary.route('/')
@diary.route('/manage')
@login_required
def manage():
    """Display a user's diary information."""
    user_diary = get_diary_today(current_user)
    return render_template('diary/manage.html', form=None, user_diarys=[user_diary])


@diary.route('/add/water-sleep', methods=['GET', 'POST'])
@login_required
def add_water_sleep():
    form = WaterSleepForm()
    user_diary = get_diary_today(current_user)
    water_sleep = user_diary.water_sleeps.first()
    if water_sleep is None:
        water_sleep = WaterSleep()
        user_diary.water_sleeps.append(water_sleep)
        db.session.add(user_diary)
        db.session.commit()
    if form.validate_on_submit():
        water_sleep.sleep = form.sleep.data
        water_sleep.water = form.water.data
        user_diary.water_sleeps.append(water_sleep)
        db.session.add(user_diary)
        db.session.commit()
        return redirect(url_for('diary.manage'))
    form.sleep.data = water_sleep.sleep
    form.water.data = water_sleep.water
    return render_template('diary/manage.html', form=form)


@diary.route('/add/exercise', methods=['GET', 'POST'])
@login_required
def add_exercise():
    form = ExerciseForm()
    if form.validate_on_submit():
        exercise = Exercise(type=form.name.data, lap=form.laps.data)
        user_diary = get_diary_today(current_user)
        user_diary.exercises.append(exercise)
        db.session.add(user_diary)
        db.session.commit()
        return redirect(url_for('diary.manage'))
    exercises = FavoriteList.query.filter_by(user_id=current_user.id).first()
    if exercises is None:
        exercises = FavoriteList(user_id=current_user.id)
        db.session.add(exercises)
        db.session.commit()
    return render_template('diary/add_exercise.html', form=form, items=exercises.exercise.split(','))


@diary.route('/add/diet', methods=['GET', 'POST'])
@login_required
def add_diet():
    form = DietForm()
    if form.validate_on_submit():
        diet = Diet(type=form.name.data, fullness=form.fullness.data)
        user_diary = get_diary_today(current_user)
        user_diary.diets.append(diet)
        db.session.add(user_diary)
        db.session.commit()
        return redirect(url_for('diary.manage'))
    lists = FavoriteList.query.filter_by(user_id=current_user.id).first()
    if lists is None:
        lists = FavoriteList(user_id=current_user.id)
        db.session.add(lists)
        db.session.commit()
    return render_template('diary/add_diet.html', form=form, items=lists.diet.split(','))


@diary.route('/manage/favorite-list/<int:type_num>', methods=['GET', 'POST'])
@login_required
def manage_favorite_list(type_num):
    form = FavoriteListForm()
    lists = FavoriteList.query.filter_by(user_id=current_user.id).first()
    if form.validate_on_submit():
        lists.exercise = form.exercise.data.strip().replace(' ', '', 20)
        lists.diet = form.diet.data.strip().replace(' ', '', 20)
        db.session.add(lists)
        db.session.commit()
        flash('즐겨찾기가 새로 저장되었습니다.', 'form-success')
        if type_num == 0:
            return redirect(url_for('diary.add_exercise'))
        else:
            return redirect(url_for('diary.add_diet'))
    form.exercise.data = lists.exercise
    form.diet.data = lists.diet
    return render_template('diary/favorite_list.html', form=form)


@diary.route('/diary-book')
@login_required
def diary_book():
    user_diarys = Diary.query.filter_by(user_id=current_user.id).order_by(desc(Diary.datetime)).all()
    return render_template('diary/manage.html', form=None, user_diarys=user_diarys)
