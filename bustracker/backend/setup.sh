#!/bin/bash
echo "============================================"
echo " BusTrack - Setup Script (Linux/macOS)"
echo "============================================"
echo

if ! command -v python3 &>/dev/null; then
  echo "ERROR: Python 3 required. Install from https://python.org"
  exit 1
fi

echo "[1/5] Creating virtual environment..."
python3 -m venv venv

echo "[2/5] Activating..."
source venv/bin/activate

echo "[3/5] Installing dependencies..."
pip install -r requirements.txt -q

echo "[4/5] Running migrations..."
python manage.py makemigrations core
python manage.py migrate

echo
echo "[5/5] Create admin account"
echo "============================================"
python manage.py createsuperuser
python manage.py fix_superuser_roles

echo
echo "============================================"
echo " Done! Start server with:"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo " Then open: http://127.0.0.1:8000"
echo "============================================"
