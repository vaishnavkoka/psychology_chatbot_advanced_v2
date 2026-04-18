@echo off
echo Starting Image Mutation Tool...
echo.

REM Start backend in new window
echo Starting backend server...
cd backend
call venv\Scripts\activate
start "Backend" python app.py

timeout /t 3

REM Start frontend in new window
echo Starting frontend...
cd ..\frontend
start "Frontend" npm start

echo.
echo Backend running on http://localhost:5000
echo Frontend running on http://localhost:3000
echo.
pause
