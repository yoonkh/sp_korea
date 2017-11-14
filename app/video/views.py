from flask import request, json, render_template

from . import video


@video.route('/')
def index():
    return render_template("diary/video_page.html")
