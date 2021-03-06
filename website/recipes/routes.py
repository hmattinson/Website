from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from flask_login import current_user, login_required
from website import db
from website.models import Recipe
from website.recipes.forms import RecipeForm, RecipeFilterForm
from website.recipes.utils import save_picture
import os
import flask_sqlalchemy

recipes = Blueprint('recipes', __name__)

@recipes.route("/recipe/new", methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        picture_file = save_picture(form.picture.data)
        recipe = Recipe(title=form.title.data,
            description=form.description.data,
            time=form.time.data,
            image_file=picture_file,
            people=form.people.data,
            difficulty=form.difficulty.data,
            source_name=form.source_name.data,
            source_link=form.source_link.data,
            ingredients=form.ingredients.data,
            method=form.method.data,
            notes=form.notes.data,
            tags=",".join(form.tags.data),
            type=",".join(form.type.data))
        db.session.add(recipe)
        db.session.commit()
        flash('Your recipe has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_recipe.html', title='New Recipe',
                           form=form, legend='New Recipe')

@recipes.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe.html', title=recipe.title, recipe=recipe)

@recipes.route("/recipe/<int:recipe_id>/update", methods=['GET', 'POST'])
@login_required
def update_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    form = RecipeForm()
    if form.validate_on_submit():
        if form.picture.data:
            old_pic = recipe.image_file
            picture_file = save_picture(form.picture.data)
            recipe.image_file = picture_file
            os.remove(os.path.join(current_app.root_path, 'static/recipe_pics', old_pic))
        recipe.title = form.title.data
        recipe.description = form.description.data
        recipe.time = form.time.data
        recipe.people = form.people.data
        recipe.difficulty = form.difficulty.data
        recipe.source_name = form.source_name.data
        recipe.source_link = form.source_link.data
        recipe.ingredients = form.ingredients.data
        recipe.method = form.method.data
        recipe.notes = form.notes.data
        recipe.tags = ",".join(form.tags.data)
        recipe.type = ",".join(form.type.data)
        db.session.commit()
        flash('Your recipe has been updated!', 'success')
        return redirect(url_for('recipes.recipe', recipe_id=recipe.id))
    elif request.method == 'GET':
        form.title.data = recipe.title
        form.description.data = recipe.description
        form.time.data = recipe.time
        form.people.data = recipe.people
        form.difficulty.data = recipe.difficulty
        form.source_name.data = recipe.source_name
        form.source_link.data = recipe.source_link
        form.ingredients.data = recipe.ingredients
        form.method.data = recipe.method
        form.notes.data = recipe.notes
        form.tags.data = recipe.tags.split(",")
        form.type.data = recipe.type.split(",")
    return render_template('create_recipe.html', title='Update Recipe',
                           form=form, legend='Update Recipe')


@recipes.route("/recipes", methods=["POST","GET"])
def all():
    form = RecipeFilterForm()
    if form.validate_on_submit():
        return redirect(url_for('recipes.all',
                            max=form.max_time.data,
                            min=form.min_time.data,
                            tags=form.tags.data,
                            type=form.type.data))
    else:
        # Process arguemnts
        page = request.args.get('page', 1, type=int)
        max = request.args.get('max', default=10000, type=int)
        min = request.args.get('min', default=0, type=int)
        type = request.args.getlist('type')
        tags = request.args.getlist('tags')
        # Refill form
        if max != 10000:
            form.max_time.data = max
        if min != 0:
            form.min_time.data = min
        form.tags.data = tags
        form.type.data = type
        # Do filtering
        recs = Recipe.query.filter(Recipe.time<max)\
                            .filter(Recipe.time>min)\
        # all didnt work for some reason so used de morgans
        type_ids = [r.id for r in recs if not any([not t in r.type.split(",") for t in type])]
        tags_ids = [r.id for r in recs if not any([not t in r.tags.split(",") for t in tags])]
        recs = recs.filter(Recipe.id.in_(type_ids))\
                            .filter(Recipe.id.in_(tags_ids))\
                            .order_by(Recipe.id.desc())\
                            .paginate(page=page, per_page=10)
    return render_template('recipes.html', recipes=recs, form=form, legend="Filter")
