@echo off
echo Starting test environment for backend...

REM Start test services
echo Starting PostgreSQL and Redis test services...
docker-compose -f ../docker-compose.test.yml up -d

REM Wait for services to be ready
echo Waiting for services to be ready...
timeout /t 15 /nobreak > nul

REM Run tests
echo Running backend tests...
python run_tests.py

REM Stop test services
echo Stopping test services...
docker-compose -f ../docker-compose.test.yml down

echo Test run completed!
pause
