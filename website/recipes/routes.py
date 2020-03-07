from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from flask_login import current_user, login_required
from website import db
from website.models import Recipe
from website.recipes.forms import RecipeForm
from website.recipes.utils import save_picture

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


@recipes.route("/recipes")
def all():
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.order_by(Recipe.id.desc()).paginate(page=page, per_page=10)
    return render_template('recipes.html', recipes=recipes)
