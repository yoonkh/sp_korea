import os
import types

from flask import render_template, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename, redirect

from app.models import Diary
from app.uploads import check_files, upload_files
from .forms import DiaryForm, UploadForm, DiaryFormPhoto, FitForm, FoodForm, FoodFormPhoto, WaterForm, SleepForm, \
    HealthForm, EtcForm, MyquestionForm, TagForm, VideoForm, MyreviewForm, ProfileForm
from . import diary


@diary.route('/', methods=['GET', 'POST'])
def diary_view():
    """운동일지 첫 시작화면"""
    form = DiaryForm()
    if form.validate_on_submit():
        num = form.number.data
        types = form.type.data
        print(num)
        print(types)

        # f = form.photo.data
        # filename = secure_filename(f.filename)
        # f.save(os.path.join(
        #     diary.instance_path, 'photos', filename
        # ))

    return render_template('diary/diary_page.html', form=form)


@diary.route('/photo', methods=['GET', 'POST'])
def diary_view_photo():
    """운동일지 두번째 화면"""
    form = DiaryFormPhoto()
    # form_photo = UploadForm()
    if form.validate_on_submit():
        images = request.files.getlist("file")
        names = form.name.data
        kcals = form.kcal.data
        times = form.time.datas
        print(names)
        print(kcals)
        print(times)

    return render_template('diary/main_page.html', form=form)


@diary.route('/gif', methods=['GET', 'POST'])
def diary_view_gif():
    """운동일지 gif 화면"""
    form = FitForm()
    if form.validate_on_submit():
        memos = form.memo.data
        print(memos)

    return render_template('diary/fit_page.html', form=form)


@diary.route('/food', methods=['GET', 'POST'])
def diary_view_food():
    """식단일지 food_page"""
    form = FoodForm()
    if form.validate_on_submit():
        food_types = form.food_type.data
        kcal = form.kcal.data
        print(food_types)
        print(kcal)

    return render_template('diary/food_page.html', form=form)


@diary.route('/food_photo', methods=['GET', 'POST'])
def diary_view_food_photo():
    """식단일지 사진등록 페이지"""
    form = FoodFormPhoto()
    if form.validate_on_submit():
        food_names = form.food_name.data
        kcals = form.kcal.data
        print(food_names)
        print(kcals)

    return render_template('diary/food_diary_page.html', form=form)


@diary.route('/water', methods=['GET', 'POST'])
def diary_view_water():
    """물일지 페이지"""
    form = WaterForm()
    if form.validate_on_submit():
        water_types = form.water_type.data
        water_sizes = form.water_size.data
        print(water_sizes)
        print(water_types)

    return render_template('diary/water_page.html', form=form)


@diary.route('/sleep', methods=['GET', 'POST'])
def diary_view_sleep():
    """수면 일지 페이지"""
    form = SleepForm()
    if form.validate_on_submit():
        sleeps = form.sleep.data
        print(sleeps)

    return render_template('diary/sleep_page.html', form=form)


@diary.route('/health', methods=['GET', 'POST'])
def diary_view_health():
    """건강일지 혈압, 혈당, 심리 페이지"""
    form = HealthForm()
    if form.validate_on_submit():
        pressures = form.pressure.data
        print(pressures)

    return render_template('diary/health_page.html', form=form)


@diary.route('/etc', methods=['GET', 'POST'])
def diary_view_etc():
    """ETC 기타일지 페이지"""
    form = EtcForm()
    if form.validate_on_submit():
        kgs = form.kg.data
        fats = form.fat.data
        bones = form.bone.data
        smokes = form.smoke.data
        alcohols = form.alcohol.data
        bowels = form.bowel.data
        print(kgs)
        print(fats)
        print(bones)
        print(smokes)
        print(alcohols)
        print(bowels)

    return render_template('diary/etc_page.html', form=form)


@diary.route('/myquestion', methods=['GET', 'POST'])
def diary_view_myquestion():
    form = MyquestionForm()
    # if form.validate_on_submit():
    return render_template('diary/myquestion_page.html', form=form)


@diary.route('/myreview', methods=['GET', 'POST'])
def diary_view_myreview():
    form = MyreviewForm()
    return render_template('diary/myreview_page.html', form=form)


@diary.route('/video', methods=['GET', 'POST'])
def diary_view_video():
    form = VideoForm()
    return render_template('diary/video_page.html', form=form)


@diary.route('/tag', methods=['GET', 'POST'])
def diary_view_tag():
    form = TagForm()
    return render_template('diary/tag_page.html', form=form)


@diary.route('/profile', methods=['GET', 'POST'])
def diary_view_profile():
    form = ProfileForm()
    return render_template('diary/profile.html', form=form)