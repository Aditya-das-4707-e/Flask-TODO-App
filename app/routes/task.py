from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Task

tasks_bp = Blueprint('task', __name__)

@tasks_bp.route('/')
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    tasks = Task.query.filter_by(user_id=session.get('user_id')).all()
    return render_template('task.html', tasks=tasks)

@tasks_bp.route('/add', methods=['POST'])
def add_task():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    title = request.form.get('task')
    if title:
        new_task = Task(title=title, status='pending', user_id=session.get('user_id'))
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully', 'success')
    return redirect(url_for('task.view_tasks'))

@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_status(task_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
        
    task = Task.query.filter_by(id=task_id, user_id=session.get('user_id')).first()
    if task:
        if task.status == 'pending':
            task.status = 'in-progress'
        elif task.status == 'in-progress':
            task.status = 'completed'
        else:
            task.status = 'pending'
        db.session.commit()
    return redirect(url_for('task.view_tasks'))

@tasks_bp.route('/clear', methods=['POST'])
def clear_task():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
        
    Task.query.filter_by(user_id=session.get('user_id')).delete()
    db.session.commit()
    flash('All tasks cleared', 'success')
    return redirect(url_for('task.view_tasks'))
    
        
        