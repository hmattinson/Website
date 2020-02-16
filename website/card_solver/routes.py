from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from website.card_solver.forms import CardsForm
from website.card_solver.utils import solve

card_solver_blueprint = Blueprint('card_solver', __name__)

@card_solver_blueprint.route('/card_solver', methods=['GET','POST'])
def card_solver():
    form = CardsForm()
    if form.validate_on_submit():
        cards = form.cards.data.split(' ')
        target = form.target.data
        answer = solve(cards, target)
        if answer[0] == 'N':
            flash(answer, 'danger')
        else:
            flash(answer, 'success')
        return redirect(url_for('card_solver.card_solver'))
    elif request.method == 'GET':
        form.target.data = 24
    return render_template('card_solver.html', title='Card Solver',
                            form=form)
