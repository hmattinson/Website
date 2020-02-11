from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app

recipes = Blueprint('recipes', __name__)

@recipes.route('/recipe')
def recipe():
    return render_template('recipe.html', title='Login')
