# Week 3 Task Tracker API

A REST API for managing projects and tasks, built with Django and Django REST Framework.

## What it does
- Create projects and add members to them
- Create tasks inside projects, assign them to users, and track their status and due dates
- Users only see tasks in projects they own or are a member of
- Filter tasks by `status`, `project` and `assigned_to`
- Search tasks by title and description
- Order tasks by `created_at`, `due_date` or `title`
- Extra endpoints: overdue tasks and a per-project task summary
- Pagination (5 per page)
- Interactive Swagger documentation

## How to run it
```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up the database
python manage.py migrate

# 4. Create an admin user
python manage.py createsuperuser

# 5. Load demo data
python manage.py seed

# 6. Start the server
python manage.py runserver
```

## Using the API
- Swagger docs: http://127.0.0.1:8000/api/docs/
- Admin site: http://127.0.0.1:8000/admin/ (log in here first, then the API works in your browser)

| Endpoint | Description |
|---|---|
| `/api/projects/` | List and create projects |
| `/api/projects/task_summary/` | Task counts per project |
| `/api/tasks/` | List and create tasks |
| `/api/tasks/overdue/` | Tasks past their due date |

Example: `/api/tasks/?status=Pending&ordering=title&search=homepage`

## Tests
```bash
python manage.py test
```