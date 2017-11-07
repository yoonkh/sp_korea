from flask import render_template, request

from ..pattern import find_pattern
from . import survey


@survey.route('/')
def survey_index():
    return render_template('survey/index.html')


@survey.route('/<page>')
def survey_page(page):
    res_code = request.args.get('resCode', None)
    if res_code:
        return render_template('/survey/result.html', result=find_pattern(res_code))
    return render_template('/survey/'+page+'.html')
