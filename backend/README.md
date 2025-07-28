# FastAPI Backend

This is the FastAPI backend for the Internal Sea Core project.

## Features

- FastAPI framework with automatic API documentation
- SQLAlchemy ORM with PostgreSQL database
- JWT authentication
- Alembic database migrations
- CORS support for frontend integration
- Comprehensive test suite

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp env.example .env
# Edit .env with your actual configuration
```

4. Set up the database:
```bash
# Create database and run migrations
alembic upgrade head
```

5. Run the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation will be available at `http://localhost:8000/docs`

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── users.py
│   │       │   └── items.py
│   │       └── api.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/
│   │   ├── user.py
│   │   └── item.py
│   └── schemas/
│       ├── auth.py
│       ├── user.py
│       └── item.py
├── alembic/
├── tests/
├── main.py
├── requirements.txt
└── README.md
```

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/token` - Get access token
- `GET /api/v1/users/` - Get all users (authenticated)
- `GET /api/v1/users/me` - Get current user info
- `GET /api/v1/items/` - Get all items (authenticated)
- `POST /api/v1/items/` - Create new item (authenticated)

## Testing

Run tests with:
```bash
pytest
``` 