# FastAPI Patient Management API

A production-ready backend API built using FastAPI, PostgreSQL, and JWT authentication.

## Features

* User Registration & Login
* Secure Password Hashing (bcrypt)
* JWT Authentication
* Protected Routes
* Full CRUD Operations for Patients
* PostgreSQL Database Integration

## Tech Stack

* FastAPI
* PostgreSQL (Neon)
* SQLAlchemy
* Passlib (bcrypt)
* JWT (python-jose)

## Endpoints

### Auth

* POST /register → Register user
* POST /token → Login & get token

### Patient API (Protected)

* POST /create
* GET /patients
* GET /patient/{id}
* PUT /update/{id}
* DELETE /delete/{id}

## Authentication

Use Bearer Token in Swagger `/docs` to access protected routes.

## How to Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```



