from flask import render_template, request
from flask_login import current_user

from .. import db
from ..models.survey import Survey
from .pattern import find_pattern
from . import survey


@survey.route('/')
def survey_index():
    return render_template('survey/index.html')


@survey.route('/<page>')
def survey_page(page):
    res_code = request.args.get('resCode', None)
    if res_code:
        if current_user.is_authenticated:
            survey_result = Survey(user_id=current_user.id, code=res_code)
            db.session.add(survey_result)
            db.session.commit()
        return render_template('/survey/result.html', result=find_pattern(res_code))
    return render_template('/survey/'+page+'.html')
