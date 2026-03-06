from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Task

tasks_bp = Blueprint('task', __name__)

@tasks_bp.route('/')
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@tasks_bp.route('/add', methods=['POST'])
def add_task():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    title = request.form.get('title')
    