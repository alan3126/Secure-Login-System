# Secure Login System

A secure web-based authentication system developed using Python Flask and SQLite.

## Features

- User registration
- Secure password hashing using bcrypt
- User login authentication
- Password validation
- Input validation
- SQL injection protection using parameterized SQL queries
- CSRF protection
- Secure session management
- Protected dashboard
- Logout functionality
- Environment-based secret key configuration
- Secure session cookie settings

## Technologies Used

- Python
- Flask
- SQLite
- Flask-Bcrypt
- Flask-WTF
- python-dotenv
- HTML
- CSS

## Project Structure

```text
Secure-Login-System/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── static/
│   └── style.css
│
└── templates/
    ├── login.html
    ├── register.html
    └── dashboard.html