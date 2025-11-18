# Schedule Project — API for Timetable

This is a Django REST Framework project for managing and querying school timetables. It provides a fully-featured backend with filtering and search capabilities, suitable for integrating with a frontend (React, Vue, etc.) or mobile app.

---

## Features

- Full REST API for school timetable entries.
- Filtering by:
  - Teacher name
  - Week number
  - Day number
  - Group name
  - Faculty name
  - Course number
  - Lesson number
- Search and query timetable entries efficiently.
- Optimized queries with `select_related`.
- CORS enabled for frontend integration.
- Swagger/OpenAPI-ready endpoints.

---

## Requirements

- Python 3.10+
- Django 5.x
- Django REST Framework
- django-filter
- psycopg2-binary (if using PostgreSQL)
- django-cors-headers

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/DovletEmin/Schedule.git
cd Schedule
```

2. Create virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser to access admin:

```bash
python manage.py createsuperuser
```

6. Run server:

```bash
python manage.py runserver
```

---

## API Endpoints

### Get timetable for a specific week and day

```
GET /api/week/<week_number>/<day_number>/
```

**Example:** `/api/week/1/2/` returns schedule for week 1, day 2.

### Search and filter timetable

```
GET /api/timetable/search/?teacher=<name>&week=<number>&day=<number>&group=<name>&faculty=<name>&course=<number>&lesson_number=<number>
```

**Example:** `/api/timetable/search/?week=1&day=2&teacher=Ali&faculty=Informatics&group=A`

**Available filters:**

- `teacher` (partial match)
- `week` (week number)
- `day` (day number)
- `group` (partial match)
- `faculty` (partial match)
- `course` (number)
- `lesson_number` (number)

---

## Admin Panel

Accessible at `/admin/`. Use the superuser credentials.

- Manage Faculties, Courses, Groups, Teachers, Weeks, Days, Lesson Types, Lesson Numbers.
- Add Timetable Entries easily with FK relations.
- Inline and search filters available.

---

## CORS

CORS is enabled in settings (`django-cors-headers`) for easy frontend integration.

- In development, all origins are allowed.
- In production, specify allowed origins in `CORS_ALLOWED_ORIGINS`.

---

## Project Structure

```
src/
├─ src/       # Django project settings
├─ timetable/             # App for timetable
│  ├─ admin.py            # Admin setup
│  ├─ models.py           # Models
│  ├─ serializers.py      # DRF serializers
│  ├─ filters.py          # Filters for search
│  ├─ views.py            # API views
│  ├─ urls.py             # API urls
│  └─ tests.py            # Unit tests
│
├─ manage.py
└─ requirements.txt
```

---

## Contact

Dovlet Eminov — dovlet.eminov26.02@gmail.com

GitHub: [https://github.com/DovletEmin](https://github.com/DovletEmin)
