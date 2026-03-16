from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists', 'error')
            return redirect(url_for('auth.register'))
            
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. You can now login.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            flash('Login successful', 'success')
            session['user'] = username
            session['user_id'] = user.id
            return redirect(url_for('task.view_tasks'))
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('auth.login'))
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    flash('Logout successful', 'success')
    return redirect(url_for('auth.login'))
