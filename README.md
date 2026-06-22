# FoodOrder

A simple Django-based food ordering web application that provides user registration and authentication, browsing a menu, adding items to a cart, and placing orders. This repository contains the Django project and a single app (core) with templates and static assets.

## Key features
- User registration & login
- Menu browsing
- Shopping cart
- Order placement (basic flow)

## Tech stack
- Python
- Django
- SQLite (default dev database)
- HTML/CSS for frontend templates

## Repository structure

root
├─ .gitignore
├─ db.sqlite3
├─ manage.py
├─ requirements.txt
├─ core/
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ serializers.py
│  ├─ signals.py
│  ├─ tests.py
│  ├─ views.py
│  └─ migrations/
├─ foodorder/
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
└─ templents/
   ├─ base.html
   ├─ cart.html
   ├─ home.html
   ├─ login.html
   ├─ menu.html
   ├─ register.html
   └─ static/
      ├─ css/
      │  ├─ app.css
      │  ├─ home.css
      │  ├─ login.css
      │  ├─ menu.css
      │  ├─ register.css
      │  └─ style.css
      └─ images/
         └─ bg.jpeg

Note: `db.sqlite3` is included in the repo currently (development DB). For production you should NOT commit your database file—add it to .gitignore and use a proper database server.

## Setup and development

Below are commands to get the project running locally. Replace `python3` with `python` on Windows if needed.

1. Clone the repository

   git clone https://github.com/developerkomalavhad/foodorder.git
   cd foodorder

2. Create and activate a virtual environment

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate

   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

3. Install dependencies

   pip install -r requirements.txt

4. Configuration

   - The project currently uses settings in `foodorder/settings.py`. For development the default SQLite DB (`db.sqlite3`) is used.
   - IMPORTANT: Do not expose SECRET_KEY or DEBUG= True in production. Use environment variables or a `.env` file.

5. Apply migrations

   python manage.py makemigrations
   python manage.py migrate

6. Create a superuser (admin)

   python manage.py createsuperuser

7. Run the development server

   python manage.py runserver

8. Run tests

   python manage.py test

9. Collect static files (if you want to serve static from STATIC_ROOT)

   python manage.py collectstatic

## Common management commands
- Start server: python manage.py runserver
- Make migrations: python manage.py makemigrations
- Apply migrations: python manage.py migrate
- Create superuser: python manage.py createsuperuser
- Run tests: python manage.py test
- Open Django shell: python manage.py shell
- Collect static: python manage.py collectstatic

## Notes & recommendations
- Remove `db.sqlite3` from the repository and add it to `.gitignore` before sharing or deploying. The presence of `db.sqlite3` can leak data and increase repo size.
- Add a `.env` to store sensitive settings (SECRET_KEY, DEBUG, DATABASE_URL) and update `foodorder/settings.py` to read from environment variables.
- Consider using `django-environ` or `python-decouple` for environment configuration.
- Add a License (e.g., MIT) and a CONTRIBUTING.md if you want community contributions.

## Contributing
1. Fork the repository
2. Create a branch: git checkout -b feature/your-feature
3. Commit your changes and open a pull request

## Contact
If you'd like, I can help:
- Remove db.sqlite3 and add migration-only setup
- Add a .env example and update settings.py to use env vars
- Improve templates and accessibility

