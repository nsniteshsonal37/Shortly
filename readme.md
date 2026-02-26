# Shortly

Shortly is a collaborative, production-style URL shortener backend built using a microservices architecture.

The project is designed to demonstrate real backend engineering practices: service separation, stateless authentication, database migrations, containerization, and deployable infrastructure.

## Architecture

The system consists of two independent FastAPI services:

### Auth Service
Handles:
- User registration
- Login
- Password hashing (bcrypt)
- JWT access token generation
- Token verification endpoint for other services

### URL Service
Handles:
- URL shortening
- Redirect resolution
- User-owned links
- Per-user link management
- Authentication via the Auth Service (service-to-service validation)

Each service has its own PostgreSQL database and communicates over HTTP inside a Docker network.

## Key Features

- FastAPI REST APIs
- JWT stateless authentication
- Microservice communication
- Separate databases per service
- Alembic database migrations
- Docker & Docker Compose orchestration
- Automatic schema upgrades on startup
- Ready for CI/CD deployment (Render)

## Tech Stack

- Python 3.13.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker / Docker Compose
- JWT (python-jose)
- Passlib (bcrypt)

## Running Locally

```bash
git clone <repo>
cd shortly
cp auth-service/.env.example auth-service/.env
cp url-service/.env.example url-service/.env
docker compose up --build