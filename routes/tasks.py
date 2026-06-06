from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from models import Task
from forms import TaskForm
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("/")
@login_required
def list_tasks():
    filter_by = request.args.get("filter", "all")
    category = request.args.get("category", "")

    query = Task.query.filter_by(user_id=current_user.id)

    if filter_by == "pending":
        query = query.filter_by(is_complete=False)
    elif filter_by == "completed":
        query = query.filter_by(is_complete=True)

    if category:
        query = query.filter_by(category=category)

    tasks = query.order_by(Task.created_at.desc()).all()
    # Collect all categories for the filter sidebar
    all_categories = (
        Task.query.with_entities(Task.category)
        .filter_by(user_id=current_user.id)
        .distinct()
        .all()
    )
    categories = sorted({c[0] for c in all_categories if c[0]})
    return render_template(
        "tasks/list.html",
        tasks=tasks,
        current_filter=filter_by,
        current_category=category,
        categories=categories,
    )


@tasks_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data or "",
            due_date=form.due_date.data,
            priority=form.priority.data,
            category=form.category.data or "",
            user_id=current_user.id,
        )
        db.session.add(task)
        db.session.commit()
        flash("Task created!", "success")
        return redirect(url_for("tasks.list_tasks"))
    return render_template("tasks/form.html", form=form, title="New Task")


@tasks_bp.route("/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data or ""
        task.due_date = form.due_date.data
        task.priority = form.priority.data
        task.category = form.category.data or ""
        db.session.commit()
        flash("Task updated!", "success")
        return redirect(url_for("tasks.list_tasks"))
    return render_template("tasks/form.html", form=form, title="Edit Task", task=task)


@tasks_bp.route("/<int:task_id>/toggle", methods=["POST"])
@login_required
def toggle_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    task.is_complete = not task.is_complete
    db.session.commit()
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"success": True, "is_complete": task.is_complete})
    flash(f"Task marked as {'complete' if task.is_complete else 'pending'}.", "success")
    return redirect(url_for("tasks.list_tasks"))


@tasks_bp.route("/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.", "info")
    return redirect(url_for("tasks.list_tasks"))
