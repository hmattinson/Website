from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from website.models import User


class CardsForm(FlaskForm):
    cards = StringField('Cards (space separated)',
                        validators=[DataRequired()])
    target = IntegerField('Target',
                            validators=[DataRequired()])
    submit = SubmitField('Calculate')
