from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SelectField, DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional


class LoginForm(FlaskForm):
    """User login form."""
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    """User registration form."""
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=80)],
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password")],
    )


class TaskForm(FlaskForm):
    """Create / edit task form."""
    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    description = TextAreaField("Description", validators=[Optional()])
    due_date = DateTimeLocalField("Due Date", validators=[Optional()], format="%Y-%m-%dT%H:%M")
    priority = SelectField(
        "Priority",
        choices=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        default="medium",
    )
    category = StringField("Category", validators=[Optional(), Length(max=100)])


class NoteForm(FlaskForm):
    """Create / edit note form."""
    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    content = TextAreaField("Content", validators=[Optional()])


class ReminderForm(FlaskForm):
    """Create / edit reminder form."""
    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    reminder_datetime = DateTimeLocalField(
        "Reminder Date & Time",
        validators=[DataRequired()],
        format="%Y-%m-%dT%H:%M",
    )
