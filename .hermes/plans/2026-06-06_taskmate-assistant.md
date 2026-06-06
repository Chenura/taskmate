# TaskMate — Personal Assistant App Implementation Plan

> **Goal:** Build and deploy a personal assistant web app with task management, notes, and reminders using Flask + SQLite + vanilla HTML/CSS/JS.

**Architecture:** Monolithic Flask app with SQLAlchemy ORM, Jinja2 templates, and a responsive CSS grid layout. SQLite for development, designed to swap to PostgreSQL for production deployment on Render/Railway.

**Tech Stack:**
- Python 3.11+ / Flask 3.x
- Flask-SQLAlchemy, Flask-Login (auth)
- SQLite (dev) / PostgreSQL (prod)
- Vanilla HTML/CSS/JS (no frontend framework — keep it simple)
- Jinja2 templating with template inheritance
- Gunicorn (prod server)
- Render.com (deployment)

---

## Project Structure

```
C:\Users\chenu\taskmate/
├── app.py                    # Flask factory
├── config.py                 # Configuration classes
├── models.py                 # SQLAlchemy models
├── forms.py                  # WTForms for validation
├── requirements.txt          # Python dependencies
├── wsgi.py                   # Gunicorn entry point
├── Procfile                  # Render deployment
├── runtime.txt               # Python version for Render
├── .env.example              # Environment template
├── routes/
│   ├── __init__.py           # Blueprint registration
│   ├── auth.py               # Login / Register / Logout
│   ├── tasks.py              # Task CRUD
│   ├── notes.py              # Note CRUD
│   └── reminders.py          # Reminder CRUD
├── templates/
│   ├── base.html             # Layout: nav, sidebar, content
│   ├── dashboard.html        # Home — pending tasks, recent notes, upcoming reminders
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── tasks/
│   │   ├── list.html
│   │   ├── form.html         # Create + Edit (shared)
│   │   └── detail.html
│   ├── notes/
│   │   ├── list.html
│   │   ├── form.html         # Create + Edit (shared)
│   │   └── detail.html
│   └── reminders/
│       ├── list.html
│       └── form.html
└── static/
    ├── css/
    │   └── style.css         # All styling (responsive, dark/light toggle)
    └── js/
        └── app.js            # UI interactions
```

---

## Task Breakdown

### Task 1: Project Setup & Skeleton

**Objective:** Initialize the project directory, virtual environment, dependencies, and Flask app factory with config.

**Files:**
- Create: `C:\Users\chenu\taskmate/app.py`
- Create: `C:\Users\chenu\taskmate/config.py`
- Create: `C:\Users\chenu\taskmate/models.py`
- Create: `C:\Users\chenu\taskmate/forms.py`
- Create: `C:\Users\chenu\taskmate/requirements.txt`
- Create: `C:\Users\chenu\taskmate/routes/__init__.py`
- Create: `C:\Users\chenu\taskmate/wsgi.py`
- Create: `C:\Users\chenu\taskmate/Procfile`
- Create: `C:\Users\chenu\taskmate/runtime.txt`
- Create: `C:\Users\chenu\taskmate/.env.example`

`requirements.txt`:
```
Flask==3.1.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.2
WTForms==3.2.1
python-dotenv==1.1.0
email-validator==2.2.0
gunicorn==23.0.0
```

`config.py`:
```python
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'taskmate.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
```

**Verification:** `pip install -r requirements.txt` succeeds, `flask run` starts without error.

---

### Task 2: Database Models

**Objective:** Define SQLAlchemy models: User, Task, Note, Reminder.

**File:** `C:\Users\chenu\taskmate/models.py`

Models:
- **User**: id, username (unique), email (unique), password_hash, created_at
- **Task**: id, title, description, due_date, priority (low/medium/high), is_complete, category, user_id (FK), created_at, updated_at
- **Note**: id, title, content (text), user_id (FK), created_at, updated_at
- **Reminder**: id, title, reminder_datetime, is_fired, task_id (FK, nullable), user_id (FK), created_at

Relationships: User has tasks, notes, reminders cascading delete.

**Verification:** Flask shell can import models and create tables.

---

### Task 3: Authentication (Login / Register / Logout)

**Objective:** User registration and login using Flask-Login + Werkzeug password hashing.

**Files:**
- Create: `routes/auth.py`
- Create: `templates/auth/login.html`
- Create: `templates/auth/register.html`
- Modify: `app.py` (register blueprints)
- Modify: `forms.py` (LoginForm, RegisterForm)

**Steps:**
1. Create LoginForm (username/email, password) and RegisterForm (username, email, password, confirm_password) in forms.py
2. Build `routes/auth.py` with `/login`, `/register`, `/logout` routes
3. Create login.html and register.html templates
4. Use `@login_required` decorator on protected routes

**Verification:** Can register a new account, log in, see dashboard, and log out.

---

### Task 4: Base Template & Dashboard

**Objective:** Create the base layout with nav sidebar and a dashboard showing overview stats.

**Files:**
- Create: `templates/base.html`
- Create: `templates/dashboard.html`
- Create: `static/css/style.css`
- Modify: `app.py` (dashboard route)

Dashboard shows:
- Pending tasks count and list (top 5)
- Recent notes (top 5) with titles and dates
- Upcoming reminders (next 5)
- Quick-add button for each section

**Verification:** After login, dashboard loads with correct stats.

---

### Task 5: Task Management (CRUD)

**Objective:** Full CRUD for tasks — create, read, update, delete — with priority, due dates, categories, and completion toggle.

**Files:**
- Create: `routes/tasks.py`
- Create: `templates/tasks/list.html`
- Create: `templates/tasks/form.html`
- Create: `templates/tasks/detail.html`
- Modify: `app.py` (register blueprint)

Features: Filter by status/category, AJAX complete toggle, overdue highlighting.

**Verification:** Can create, view, edit, complete, and delete tasks.

---

### Task 6: Notes Management (CRUD)

**Objective:** Full CRUD for notes.

**Files:**
- Create: `routes/notes.py`
- Create: `templates/notes/list.html`
- Create: `templates/notes/form.html`
- Create: `templates/notes/detail.html`
- Modify: `app.py` (register blueprint)

**Verification:** Can create, view, edit, and delete notes.

---

### Task 7: Reminders Management (CRUD)

**Objective:** Full CRUD for reminders, optionally linked to a task.

**Files:**
- Create: `routes/reminders.py`
- Create: `templates/reminders/list.html`
- Create: `templates/reminders/form.html`
- Modify: `app.py` (register blueprint)

Features: Chronological list, optional task link, mark as fired, visual distinction.

**Verification:** Can create reminders, link to tasks, edit, delete.

---

### Task 8: Polish UI / UX

**Objective:** Make the app look polished with responsive design and smooth interactions.

**Files:**
- Modify: `static/css/style.css`
- Create: `static/js/app.js`
- Modify: templates as needed

Features: Responsive sidebar, color-coded priorities, confirmation modals, toast notifications.

**Verification:** App looks good on desktop and mobile.

---

### Task 9: Deploy to Render

**Objective:** Deploy the app to Render.com free tier and verify it works.

**Steps:**
1. Create a GitHub repository and push code
2. Create a Render Web Service linked to the GitHub repo
3. Set env vars (SECRET_KEY, DATABASE_URL for PostgreSQL)
4. Deploy and verify the live URL

**Verification:** App accessible at Render URL, all features work.

---

## Design Decisions

- **Flask blueprints** — clean route separation per feature
- **Flask-Login** — battle-tested session auth, no JWT complexity
- **SQLite → PostgreSQL** — seamless swap via DATABASE_URL env var
- **Vanilla JS** — no framework overhead for this scope
- **No push notifications** for MVP — reminders page serves as manual check-in

## Verification Checklist

- [ ] Register → login → see empty dashboard
- [ ] Create task, complete it, edit, delete
- [ ] Create note, view, edit, delete
- [ ] Create reminder (standalone + linked to task)
- [ ] Log out → log back in — data persists
- [ ] Works on mobile viewport
- [ ] Works on Render from fresh database
