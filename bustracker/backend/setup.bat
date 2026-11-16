@echo off
echo ============================================
echo  BusTrack - Setup Script (Windows)
echo ============================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install from https://python.org
    pause & exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv

echo [2/5] Activating...
call venv\Scripts\activate.bat

echo [3/5] Installing dependencies...
pip install -r requirements.txt -q

echo [4/5] Running migrations...
python manage.py makemigrations core
python manage.py migrate

echo.
echo [5/5] Create admin account
echo ============================================
python manage.py createsuperuser
python manage.py fix_superuser_roles

echo.
echo ============================================
echo  Done! Start server with:
echo    venv\Scripts\activate
echo    python manage.py runserver
echo  Then open: http://127.0.0.1:8000
echo ============================================
pause
