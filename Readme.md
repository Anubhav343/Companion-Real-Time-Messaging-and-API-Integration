# Companion - Community Discussion Platform

Companion is a full-stack community discussion platform inspired by Reddit, built as a long-term learning project to explore modern Django backend development.

Users can create discussion rooms, participate in conversations, browse topics, manage profiles, and interact through real-time chat. The project gradually evolved from a classic Django monolith into a system that also exposes REST APIs and supports WebSocket-based communication using Django Channels.

## Features

* User registration and authentication
* Custom user profiles
* Room creation, updating, and deletion
* Topic-based discussion rooms
* Search and filtering functionality
* Real-time messaging
* Typing indicators
* REST API built with Django REST Framework
* JWT authentication for API access
* OpenAPI / Swagger documentation
* Role-based permissions and access control

## Tech Stack

### Backend

* Django
* Django REST Framework (DRF)
* Django Channels
* Simple JWT

### Communication

* REST APIs
* WebSockets
* ASGI

### Database

* SQLite (Development)

### Documentation

* Swagger / OpenAPI (drf-spectacular)

### Version Control

* Git
* GitHub

## Project Architecture

The application contains two communication layers:

### Traditional HTTP Layer

Used for:

* Page rendering
* Authentication
* CRUD operations
* API requests

```text
Browser
   ↓
Django / DRF
   ↓
ORM
   ↓
Database
```

### Real-Time Layer

Used for:

* Chat messages
* Typing indicators

```text
Browser
   ↓
WebSocket
   ↓
Django Channels
   ↓
ASGI
   ↓
Channel Layer
```

This project was my introduction to asynchronous programming concepts in Django, including ASGI, event loops, channel layers, and real-time communication patterns.

## API Features

The REST API includes:

* JWT Authentication
* Room CRUD endpoints
* Message endpoints
* User endpoints
* Search and filtering
* Pagination
* Permission-based access control
* Auto-generated Swagger documentation

## Key Concepts Explored

Throughout this project I focused on understanding how backend systems work under the hood rather than simply building features.

Topics explored include:

* Django ORM
* Request lifecycle
* REST API design
* Serializers
* Authentication and authorization
* JWT token workflows
* Query optimization and filtering
* API permissions
* ASGI architecture
* WebSockets
* Django Channels
* Real-time communication
* Redis-based channel layers
* Environment-based configuration
* Deployment preparation and security hardening

## Running Locally

Clone the repository:

```bash
git clone https://github.com/Anubhav343/Companion-Real-Time-Messaging-and-API-Integration
cd companion
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and configure the required environment variables.

Run migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

## Future Improvements

Some areas I would like to explore in future versions:

* Cloud-based media storage
* PostgreSQL deployment
* Advanced notifications
* Direct messaging
* Room moderation tools
* Frontend framework integration

## Learning Notes

This project began as a traditional Django application and gradually expanded into a platform that incorporates APIs, JWT authentication, and real-time communication. The primary goal was not only to build features, but also to understand the architectural ideas behind modern backend systems and how Django applications evolve as requirements become more complex.
