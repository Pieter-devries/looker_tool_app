from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class LiquidLinter(FlaskForm):
    liquid_text = TextAreaField('Liquid Text', validators=[DataRequired()])
    submit = SubmitField('Validate')

class DeleteMessage(FlaskForm):
    delete = SubmitField('Delete')
