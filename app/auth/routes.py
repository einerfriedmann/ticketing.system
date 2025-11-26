# This file contains the authentication routes for the application. These routes hanlde the user registration, login, and logout functionality.

from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from flask_login import login_user, logout_user, current_user
from app.forms import LoginForm, RegistrationForm
from app.models import User
from app import db
from app.auth import bp
from sqlalchemy import select

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')  # Add 'success' category
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Handle the user login
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        stmt = select(User).where(User.username == form.username.data)
        user = db.session.execute(stmt).scalars().first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        flash('You have been logged in successfully!', 'success')
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.index'))
    
    return render_template('auth/login.html', title='Login', form=form)

@bp.route('/logout')
def logout():
    # Handles the user logout
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
