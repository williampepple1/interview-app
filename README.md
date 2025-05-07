# Assessment App

A Django-based assessment application where users can take timed multiple-choice assessments.

## Features
- Admin can create assessments with multiple-choice questions
- Users can attempt assessments with a 30-second time limit per question
- Session-based assessment tracking
- SQLite database for data storage

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

The application will be available at http://127.0.0.1:8000/ 