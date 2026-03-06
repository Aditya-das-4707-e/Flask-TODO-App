from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__)

USER_CREDENTIALS = {
    "username": "admin",
    "password": "1234"
}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
            flash('Login successful', 'success')
            session['user'] = username
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('auth.login'))
            return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logout successful', 'success')
    return redirect(url_for('auth.login'))

