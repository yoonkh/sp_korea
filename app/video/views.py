from flask import render_template, abort
from flask_login import login_required

from ..models import get_random_video, Video
from . import video


@video.route('/')
@login_required
def index():
    videos = get_random_video()
    return render_template("video/video_list.html", videos=videos)


@video.route('/<int:video_id>')
@video.route('/<int:video_id>/info')
@login_required
def video_info(video_id):
    videos = Video.query.filter_by(id=video_id).first()
    if videos is None:
        abort(404)
    return render_template("video/video_page.html", videos=videos)
