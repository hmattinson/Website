from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_login import current_user
from website.models import Recipe


class RecipeForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired(),
                        Length(min=2, max=100)])
    description = StringField('Description',
                        validators=[DataRequired()])
    picture = FileField('Picture',
                        validators=[
                                    FileAllowed(['jpg', 'png'])])
    time = IntegerField('Time (minutes)',
                        validators=[DataRequired(),
                        NumberRange(0,10000)])
    people = IntegerField('People',
                        validators=[DataRequired(),
                        NumberRange(0,100)])
    difficulty = StringField('Difficulty',
                        validators=[DataRequired(),
                        Length(min=2, max=16)])
    source_name = StringField('Source',
                        validators=[Length(min=2, max=1000)])
    source_link = StringField('Link',
                        validators=[])
    ingredients = TextAreaField('Ingredients',
                        validators=[DataRequired()])
    method = TextAreaField('Method',
                        validators=[DataRequired()])
    notes = TextAreaField('Notes',
                        validators=[])
    tags = SelectMultipleField('Tags', choices = [
        ('Vegetarian','Vegetarian'),
        ('One-pot','One-pot'),
        ('Spicy','Spicy'),
        ('Hard ingredients','Hard ingredients')])
    type = SelectMultipleField('Type',choices = [
        ('Curry','Curry'),
        ('Pasta','Pasta'),
        ('Soup','Soup'),
        ('Meat','Meat'),
        ('Caserole','Caserole'),
        ('Main','Main'),
        ('Starter','Starter'),
        ('Dessert','Dessert'),
        ('Indian','India'),
        ('Thai','Thailand')])
    submit = SubmitField('Submit')
