from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from models import Note
from forms import NoteForm

notes_bp = Blueprint("notes", __name__, url_prefix="/notes")


@notes_bp.route("/")
@login_required
def list_notes():
    notes = (
        Note.query.filter_by(user_id=current_user.id)
        .order_by(Note.updated_at.desc())
        .all()
    )
    return render_template("notes/list.html", notes=notes)


@notes_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_note():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(
            title=form.title.data,
            content=form.content.data or "",
            user_id=current_user.id,
        )
        db.session.add(note)
        db.session.commit()
        flash("Note created!", "success")
        return redirect(url_for("notes.list_notes"))
    return render_template("notes/form.html", form=form, title="New Note")


@notes_bp.route("/<int:note_id>")
@login_required
def view_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    return render_template("notes/detail.html", note=note)


@notes_bp.route("/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data or ""
        db.session.commit()
        flash("Note updated!", "success")
        return redirect(url_for("notes.list_notes"))
    return render_template("notes/form.html", form=form, title="Edit Note", note=note)


@notes_bp.route("/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    db.session.delete(note)
    db.session.commit()
    flash("Note deleted.", "info")
    return redirect(url_for("notes.list_notes"))
