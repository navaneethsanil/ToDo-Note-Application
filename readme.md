# Django To-Do Project Management App

A Django-based web application for managing to-dos within projects, with the capability to export project summaries as GitHub secret gists.

## Features
1. **Project Management**: Create, view, and manage projects.
2. **To-Do Management**: Add, update, mark as complete, and delete to-dos within a project.
3. **Project Summary Export**: Export the project summary in Markdown format as a secret gist on GitHub
4. **Basic Authentication**: User signIn/singOut functionality for secure access.
5. **Local Summary Storage**: Save the exported gist file locally.

## Requirements
- Python 3.7+
- Django 4.x
- GitHub account with a Personal Access Token (for gist export functionality)

## Setup

```bash
git clone https://github.com/navaneethsanil/ToDo-Note-Application.git
cd ToDo-Note-Application

python -m venv env
source env/bin/activate  # On Windows use `source env/Scripts/activate`

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser - NOTE: There is already an admin user exists in the database, with username: admin, and password: Testing@123

# Gists setup
export GITHUB_ACCESS_TOKEN='your_github_access_token_here'  # Use `set` on Windows

python manage.py runserver
```
Run unit tests to validate application functionality
```python manage.py test```
