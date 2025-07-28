# Internal Sea Core

A modern full-stack web application built with FastAPI (backend) and React (frontend).

## Project Overview

This project consists of two main components:
- **Backend**: FastAPI-based REST API with PostgreSQL database
- **Frontend**: React TypeScript application with modern UI

## Features

### Backend (FastAPI)
- RESTful API with automatic documentation
- JWT authentication and authorization
- SQLAlchemy ORM with PostgreSQL
- Alembic database migrations
- CORS support for frontend integration
- Comprehensive test suite
- Environment-based configuration

### Frontend (React)
- Modern React 18 with TypeScript
- React Router for navigation
- Context API for state management
- JWT authentication integration
- Responsive design
- Protected routes
- Axios for API communication

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL database
- Redis (optional, for caching)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp env.example .env
# Edit .env with your actual configuration
```

5. Set up the database:
```bash
# Create database and run migrations
alembic upgrade head
```

6. Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The application will be available at `http://localhost:3000`

## Project Structure

```
internal-sea-core/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   ├── auth.py
│   │   │       │   ├── users.py
│   │   │       │   └── items.py
│   │   │       └── api.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   └── item.py
│   │   └── schemas/
│   │       ├── auth.py
│   │       ├── user.py
│   │       └── item.py
│   ├── alembic/
│   ├── tests/
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── contexts/
│   │   ├── pages/
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   └── README.md
├── LICENSE
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/token` - Get access token

### Users
- `GET /api/v1/users/` - Get all users (authenticated)
- `GET /api/v1/users/me` - Get current user info
- `GET /api/v1/users/{user_id}` - Get specific user

### Items
- `GET /api/v1/items/` - Get all items (authenticated)
- `POST /api/v1/items/` - Create new item (authenticated)
- `GET /api/v1/items/{item_id}` - Get specific item
- `PUT /api/v1/items/{item_id}` - Update item
- `DELETE /api/v1/items/{item_id}` - Delete item

## Development

### Backend Development
- Run tests: `pytest`
- Create migration: `alembic revision --autogenerate -m "description"`
- Apply migrations: `alembic upgrade head`

### Frontend Development
- Run tests: `npm test`
- Build for production: `npm run build`

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/internal_sea_core
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_URL=redis://localhost:6379
ENVIRONMENT=development
DEBUG=true
ALLOWED_HOSTS=["http://localhost:3000","http://127.0.0.1:3000"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
