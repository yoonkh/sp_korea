from flask import render_template

from ..models import Video
from . import video


@video.route('/')
def index():
    videos = Video.query.all()
    return render_template("video/video_list.html", videos=videos)


@video.route('/detail/<int:video_num>')
def video_detail(video_num):
    return render_template("video/video_page.html")
