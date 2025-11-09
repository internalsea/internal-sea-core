# Quick Start Guide

## Prerequisites

- Docker and Docker Compose installed
- Or: Node.js 16+ and Python 3.8+ (for local development)

## Running with Docker Compose (Recommended)

### Development Mode

1. **Start all services** (backend, frontend, database, redis):
   ```bash
   docker-compose up
   ```

2. **Or run in detached mode** (background):
   ```bash
   docker-compose up -d
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Backend Health Check: http://localhost:8000/health

4. **Stop all services**:
   ```bash
   docker-compose down
   ```

5. **View logs**:
   ```bash
   docker-compose logs -f
   ```

6. **Rebuild containers** (after code changes):
   ```bash
   docker-compose up --build
   ```

### Production Mode

1. **Build and start production services**:
   ```bash
   docker-compose -f docker-compose.prod.yml up --build
   ```

2. **Access the application**:
   - Frontend: http://localhost (via nginx on port 80)
   - Backend API: http://localhost/api/v1/ (proxied through nginx)

## Running Without Docker (Local Development)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional):
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Start PostgreSQL and Redis** (or use Docker):
   ```bash
   # Using Docker for just database services:
   docker-compose up postgres redis
   ```

6. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

7. **Start the backend server**:
   ```bash
   uvicorn main:app --reload
   ```

   Backend will be available at: http://localhost:8000

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```

   Frontend will be available at: http://localhost:3000

## Troubleshooting

### Port Already in Use

If ports 3000, 8000, 5432, or 6379 are already in use:

1. **Stop the conflicting service**, or
2. **Change ports in docker-compose.yml**:
   ```yaml
   ports:
     - "3001:3000"  # Change host port
   ```

### Database Connection Issues

1. **Check if PostgreSQL is running**:
   ```bash
   docker-compose ps
   ```

2. **Check database health**:
   ```bash
   docker-compose exec postgres pg_isready -U intsea
   ```

### Frontend Not Loading

1. **Check if frontend container is running**:
   ```bash
   docker-compose ps frontend
   ```

2. **Check frontend logs**:
   ```bash
   docker-compose logs frontend
   ```

3. **Rebuild frontend**:
   ```bash
   docker-compose up --build frontend
   ```

### Backend Not Responding

1. **Check backend logs**:
   ```bash
   docker-compose logs backend
   ```

2. **Test backend health**:
   ```bash
   curl http://localhost:8000/health
   ```

## Useful Commands

### Docker Compose Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View logs
docker-compose logs -f [service_name]

# Restart a service
docker-compose restart [service_name]

# Rebuild a service
docker-compose up --build [service_name]

# Execute command in container
docker-compose exec [service_name] [command]

# View running containers
docker-compose ps
```

### Backend Commands

```bash
# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"

# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/
```

### Frontend Commands

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

## Next Steps

1. Open http://localhost:3000 to see the Session page
2. The Session page will try to fetch data from `/api/v1/session/`
3. If the API is not available, the menu will turn red-grey and show "unknown" values
4. Check http://localhost:8000/docs for API documentation

