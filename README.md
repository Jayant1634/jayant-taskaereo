# Django Task Management System

This is a simple task management system built with Django and Django REST Framework. It allows users to create, view, update, and delete tasks through a web interface and a REST API.

## Features

*   Create, Read, Update, Delete (CRUD) operations for tasks.
*   REST API for task management.
*   Frontend interface built with HTML, CSS (Bootstrap), and JavaScript (jQuery).
*   Filtering and sorting capabilities for tasks (by title, creation date).
*   AJAX-powered frontend for a smooth user experience (no page reloads for filtering, creating, updating, deleting).

## Project Setup

Follow these steps to set up the project locally:

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd django-template
    ```

2.  **Create a virtual environment:**
    It's recommended to use a virtual environment to manage project dependencies.
    ```bash
    # On Windows
    python -m venv .venv
    .venv\Scripts\activate

    # On macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    Install the required Python packages using pip.
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: If `requirements.txt` doesn't exist, you might need to create it based on the installed packages: `pip freeze > requirements.txt`)*

4.  **Apply database migrations:**
    Set up the database schema.
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (optional):**
    If you want to access the Django admin interface.
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create an administrator account.

## Running the Project

1.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```

2.  **Access the application:**
    Open your web browser and navigate to `http://127.0.0.1:8000/`.

3.  **Access the API:**
    The main API endpoint for tasks is available at `http://127.0.0.1:8000/api/tasks/`.

## Testing with Postman

The API endpoints can be tested using Postman:

1. **Access the Postman Collection:**
   You can use this shared Postman collection to test all endpoints:
   [Postman Collection Link](https://jayant-6865500.postman.co/workspace/Jayant's-Workspace~d186fad4-b942-4876-800a-8fe58b43927a/collection/44457829-120beef6-e9b3-496d-9162-75f636be13e3?action=share&creator=44457829)

2. **Test the following endpoints:**
   - `GET /api/tasks/` - List all tasks
   - `GET /api/tasks/?search=<term>` - Search tasks by title
   - `GET /api/tasks/?search_date=<date>` - Filter tasks by date
   - `GET /api/tasks/?sort_by_date=true` - Sort tasks by date (newest first)
   - `POST /api/tasks/` - Create a new task
   - `GET /api/tasks/<id>/` - Retrieve a specific task
   - `PATCH /api/tasks/<id>/` - Update a task
   - `DELETE /api/tasks/<id>/` - Delete a task

## API Documentation

### Endpoints

| HTTP Method | Endpoint                 | Description                                   | Query Parameters                                              |
|-------------|--------------------------|-----------------------------------------------|---------------------------------------------------------------|
| GET         | `/api/tasks/`            | List all tasks                                | `search`: Filter by title<br>`search_date`: Filter by date<br>`sort_by_date`: Sort by date (`true` for newest first, `false` for oldest first) |
| POST        | `/api/tasks/`            | Create a new task                             | N/A                                                           |
| GET         | `/api/tasks/{id}/`       | Retrieve a specific task                      | N/A                                                           |
| PUT         | `/api/tasks/{id}/`       | Replace a task completely                     | N/A                                                           |
| PATCH       | `/api/tasks/{id}/`       | Update a task partially                       | N/A                                                           |
| DELETE      | `/api/tasks/{id}/`       | Delete a task                                 | N/A                                                           |

### Web Interface URLs

| URL                | Description                      | Named URL      |
|--------------------|----------------------------------|----------------|
| `/`                | Home page with task list         | `task-list`    |
| `/admin/`          | Django admin interface           | `admin:index`  |

## Project Documentation

### Management Commands

*   `python manage.py runserver`: Starts the Django development server.
*   `python manage.py migrate`: Applies database migrations.
*   `python manage.py makemigrations`: Creates new migration files based on model changes.
*   `python manage.py createsuperuser`: Creates an admin user.
*   `python manage.py collectstatic`: Collects static files into `STATIC_ROOT` (used for deployment).

### Viewsets

*   **`TaskViewSet` (`tasks/views.py`)**
    *   **Model:** `Task`
    *   **Serializer:** `TaskSerializer`
    *   **Permissions:** `AllowAny` (For simplicity in this example; should be adjusted for production)
    *   **Filtering:** Supports filtering by `created_date` (exact, gte, lte), searching by `title`, and ordering by `created_date`.
    *   **Functionality:** Provides standard CRUD endpoints (`list`, `create`, `retrieve`, `update`, `partial_update`, `destroy`) for tasks via the REST API. Includes logic to handle duplicate task creation requests and custom filtering/pagination logic based on query parameters.

### Serializers

*   **`TaskSerializer` (`tasks/serializers.py`)**
    *   **Model:** `Task`
    *   **Fields:** `id`, `title`, `description`, `created_date`
    *   **Functionality:** Serializes `Task` model instances into JSON format for the API and deserializes JSON data into `Task` instances for creation/updates.

### Models

*   **`Task` (`tasks/models.py`)**
    *   **Fields:**
        *   `title`: CharField - The task title
        *   `description`: TextField - Detailed description of the task
        *   `created_date`: DateTimeField - When the task was created (auto-populated)
    *   **Functionality:** Stores task information in the database.

### Request and Response Examples

#### Task Creation (POST `/api/tasks/`)

Request:
```json
{
  "title": "Task Title",
  "description": "Task Description"
}
```

Response:
```json
{
  "id": 1,
  "title": "Task Title",
  "description": "Task Description",
  "created_date": "2025-04-26T10:30:00Z"
}
```

#### Task List (GET `/api/tasks/`)

Response:
```json
[
  {
    "id": 1,
    "title": "Task Title",
    "description": "Task Description",
    "created_date": "2025-04-26T10:30:00Z"
  },
  {
    "id": 2,
    "title": "Another Task",
    "description": "Another Description",
    "created_date": "2025-04-25T10:30:00Z"
  }
]
```

## Project Structure

```
django-template/
├── .venv/               # Virtual environment directory
├── tasks/               # Django app for tasks
│   ├── migrations/      # Database migrations
│   ├── templates/       # HTML templates for the tasks app
│   │   └── tasks/
│   │       ├── base.html
│   │       └── task_list.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py        # Task model definition
│   ├── serializers.py   # Task serializer definition
│   ├── tests.py
│   ├── urls.py          # URLs specific to the tasks app
│   └── views.py         # Task views (TaskListView, TaskViewSet)
├── web_django/          # Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py      # Project settings
│   ├── urls.py          # Project-level URLs
│   └── wsgi.py
├── db.sqlite3           # SQLite database file
├── staticfiles/         # Collected static files
├── manage.py            # Django management script
├── README.md            # This file
└── requirements.txt     # Project dependencies
```

## Note on Project Cleanup

This repository has been cleaned of all irrelevant files and folders such as:
- Cache files
- Build/dist directories
- IDE-specific configuration files
- Unused virtual environments
- Temporary files

## References

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)

## Contributing

Feel free to submit pull requests or open issues for bugs or feature requests.
