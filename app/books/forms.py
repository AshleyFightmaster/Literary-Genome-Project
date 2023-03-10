from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class Booksearchform(FlaskForm):
    search = StringField('search', validators=[DataRequired()])
    submit = SubmitField()

