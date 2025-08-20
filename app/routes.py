from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from app.models import Task
from app.forms import TaskForm
from app import db
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    tasks = Task.query.order_by(Task.created_at.desc()).paginate(
        page=page, per_page=current_app.config['TASKS_PER_PAGE'], error_out=False
    )
    return render_template('index.html', tasks=tasks)

@main_bp.route('/add', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            completed=form.completed.data
        )
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('add.html', form=form)

@main_bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.completed = form.completed.data
        task.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('edit.html', form=form, task_id=task_id)

@main_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('main.index'))

@main_bp.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    db.session.commit()
    
    status = 'completed' if task.completed else 'reopened'
    flash(f'Task {status} successfully!', 'success')
    return redirect(url_for('main.index'))

@main_bp.route('/api/tasks')
def api_tasks():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return jsonify([task.to_dict() for task in tasks])

@main_bp.route('/api/task/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
def api_task_detail(task_id):
    task = Task.query.get_or_404(task_id)
    
    if request.method == 'GET':
        return jsonify(task.to_dict())
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'completed' in data:
            task.completed = data['completed']
        
        task.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Task updated successfully',
            'task': task.to_dict()
        })
    
    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Task deleted successfully'
        })

@main_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error=404, message='Page not found'), 404

@main_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', error=500, message='Internal server error'), 500
