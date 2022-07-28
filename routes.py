import forms
from datetime import timedelta
from main import app
from flask import render_template, request, url_for, flash, redirect, session, Markup
import parse


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/liquid', methods=(['GET', 'POST']))
def liquid_linter():
    form = forms.LiquidLinter()
    if form.validate_on_submit():
        session.clear()
        parse_liquid(form.liquid_text.data)
        return render_template('liquid_linter.html', form=form)
    return render_template('liquid_linter.html', form=form)

def parse_liquid(data):
    message = parse.main(data)
    for field in message:
        field_dict = field
        message = Markup(field_dict['header'])
        message += Markup(field_dict['message'])
        flash(message)





