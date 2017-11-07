from flask import render_template, request, app, url_for
# from ..models import EditableHTML
from werkzeug.utils import redirect

from pattern import find_pattern
from . import main


@main.route('/')
def basic():
    return redirect(url_for('.survey_index'))


@main.route('/survey')
def survey_index():
    return render_template('survey/index.html')


@main.route('/survey/<page>')
def survey_page(page):
    res_code = request.args.get('resCode', None)
    if res_code:
        return render_template('/survey/result.html', result=find_pattern(res_code))
    return render_template('/survey/' + page + '.html')



# 기존 flask-base views.py입니다
# from flask import render_template
# from ..models import EditableHTML
#
# from . import main
#
#
# @main.route('/')
# def index():
#     return render_template('main/index.html')
#
#
# @main.route('/about')
# def about():
#     editable_html_obj = EditableHTML.get_editable_html('about')
#     return render_template('main/about.html',
#                            editable_html_obj=editable_html_obj)
