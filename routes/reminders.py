from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models import Reminder, Task
from forms import ReminderForm

reminders_bp = Blueprint("reminders", __name__, url_prefix="/reminders")


@reminders_bp.route("/")
@login_required
def list_reminders():
    reminders = (
        Reminder.query.filter_by(user_id=current_user.id)
        .order_by(Reminder.reminder_datetime.asc())
        .all()
    )
    return render_template("reminders/list.html", reminders=reminders)


@reminders_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_reminder():
    form = ReminderForm()
    # Add optional task selector
    tasks = Task.query.filter_by(
        user_id=current_user.id, is_complete=False
    ).order_by(Task.title).all()

    if form.validate_on_submit():
        task_id = request.form.get("task_id", type=int)
        reminder = Reminder(
            title=form.title.data,
            reminder_datetime=form.reminder_datetime.data,
            task_id=task_id if task_id else None,
            user_id=current_user.id,
        )
        db.session.add(reminder)
        db.session.commit()
        flash("Reminder created!", "success")
        return redirect(url_for("reminders.list_reminders"))
    return render_template(
        "reminders/form.html", form=form, tasks=tasks, title="New Reminder"
    )


@reminders_bp.route("/<int:reminder_id>/edit", methods=["GET", "POST"])
@login_required
def edit_reminder(reminder_id):
    reminder = Reminder.query.filter_by(
        id=reminder_id, user_id=current_user.id
    ).first_or_404()
    form = ReminderForm(obj=reminder)
    tasks = Task.query.filter_by(
        user_id=current_user.id, is_complete=False
    ).order_by(Task.title).all()

    if form.validate_on_submit():
        task_id = request.form.get("task_id", type=int)
        reminder.title = form.title.data
        reminder.reminder_datetime = form.reminder_datetime.data
        reminder.task_id = task_id if task_id else None
        db.session.commit()
        flash("Reminder updated!", "success")
        return redirect(url_for("reminders.list_reminders"))
    return render_template(
        "reminders/form.html",
        form=form,
        tasks=tasks,
        title="Edit Reminder",
        reminder=reminder,
    )


@reminders_bp.route("/<int:reminder_id>/fire", methods=["POST"])
@login_required
def fire_reminder(reminder_id):
    reminder = Reminder.query.filter_by(
        id=reminder_id, user_id=current_user.id
    ).first_or_404()
    reminder.is_fired = True
    db.session.commit()
    flash("Reminder marked as done.", "success")
    return redirect(url_for("reminders.list_reminders"))


@reminders_bp.route("/<int:reminder_id>/delete", methods=["POST"])
@login_required
def delete_reminder(reminder_id):
    reminder = Reminder.query.filter_by(
        id=reminder_id, user_id=current_user.id
    ).first_or_404()
    db.session.delete(reminder)
    db.session.commit()
    flash("Reminder deleted.", "info")
    return redirect(url_for("reminders.list_reminders"))
