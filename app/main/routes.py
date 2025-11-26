from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.main import bp

@bp.route('/')

@bp.route('/index')

# This makes sure the user is logged in to access the homepage
@login_required
def index():
    return render_template('main/index.html', title='Home', user=current_user)
