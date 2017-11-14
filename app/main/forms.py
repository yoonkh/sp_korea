# import os
# import imghdr
# from flask import Flask, render_template, app
# from flask_wtf import FlaskForm
# from wtforms import FileField, SubmitField, ValidationError
#
#
# class UploadForm(FlaskForm):
#     image_file = FileField('Image file')
#     submit = SubmitField('Submit')
#
#     def validate_image_file(self, field):
#         if field.data.filename[-4:].lower() != '.jpg':
#             raise ValidationError('Invalid file extension')
#         if imghdr.what(field.data) != 'jpeg':
#             raise ValidationError('Invalid image format')
#
