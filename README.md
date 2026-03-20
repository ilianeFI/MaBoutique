Maboutique

Maboutique is a work-in-progress e-commerce web application built with Django. It currently uses MySQL for the database, with a potential future switch to PostgreSQL.

Features (Planned / In Progress)

Product catalog with categories

Shopping cart and checkout system

User authentication (signup, login, logout)

Admin dashboard for managing products and orders

Responsive design for desktop and mobile

Tech Stack

Backend: Django (Python)

Database: MySQL (switching to PostgreSQL planned)

Frontend: HTML, CSS, JavaScript

Environment: .env file for sensitive configurations (not committed)

Setup Instructions

Clone the repository:

git clone https://github.com/ilianeFI/Maboutique.git
cd Maboutique

Create and activate a virtual environment:

python -m venv .venv
source .venv/bin/activate    # Linux / macOS
.venv\Scripts\activate       # Windows

Install dependencies:

pip install -r requirements.txt

Create a .env file based on .env.example and fill in your database and Django secrets. Example variables:

DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=your_secret_key
DEBUG=True

Apply migrations:

python manage.py migrate

Run the development server:

python manage.py runserver
Notes

Do not commit your .env file or any sensitive data.

Static files and media uploads are ignored in Git.

This project is under active development. Features and database setups may change.
