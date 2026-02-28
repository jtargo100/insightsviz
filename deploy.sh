#!/usr/bin/env bash
#
# PythonAnywhere Deployment Script
# =================================
# Run this script on PythonAnywhere after cloning the repo.
#
# Usage:
#   bash deploy.sh            # Full setup (first time)
#   bash deploy.sh update     # Pull latest & restart
#

set -e

# Configuration
PYTHONANYWHERE_USER="insightsvisualization"
PROJECT_DIR="/home/${PYTHONANYWHERE_USER}/insightsvisualization"
VENV_DIR="/home/${PYTHONANYWHERE_USER}/.virtualenvs/insightsvisualization"
SRC_DIR="${PROJECT_DIR}/src"
PYTHON_VERSION="3.10"

echo "============================================"
echo "  Insights Visualization — Deployment"
echo "============================================"

if [ "$1" = "update" ]; then
    echo ""
    echo ">>> Pulling latest changes..."
    cd "$PROJECT_DIR"
    git pull origin main

    echo ""
    echo ">>> Installing dependencies..."
    source "${VENV_DIR}/bin/activate"
    pip install -r requirements.txt

    echo ""
    echo ">>> Running migrations..."
    cd "$SRC_DIR"
    python -m django migrate --settings=insightsvisualization.website.settings

    echo ""
    echo ">>> Collecting static files..."
    python -m django collectstatic --noinput --settings=insightsvisualization.website.settings

    echo ""
    echo ">>> Reloading web app..."
    touch /var/www/${PYTHONANYWHERE_USER}_pythonanywhere_com_wsgi.py

    echo ""
    echo "Done! Your site is updated at https://${PYTHONANYWHERE_USER}.pythonanywhere.com"
    exit 0
fi

# Full setup
echo ""
echo ">>> Step 1: Clone or update repository"
if [ ! -d "$PROJECT_DIR" ]; then
    echo "    Please clone your repository first:"
    echo "    git clone <your-repo-url> $PROJECT_DIR"
    exit 1
fi

echo ""
echo ">>> Step 2: Create virtual environment"
if [ ! -d "$VENV_DIR" ]; then
    mkvirtualenv --python=/usr/bin/python${PYTHON_VERSION} insightsvisualization
else
    source "${VENV_DIR}/bin/activate"
fi

echo ""
echo ">>> Step 3: Install dependencies"
cd "$PROJECT_DIR"
pip install -r requirements.txt

echo ""
echo ">>> Step 4: Run migrations"
cd "$SRC_DIR"
python -m django migrate --settings=insightsvisualization.website.settings

echo ""
echo ">>> Step 5: Collect static files"
python -m django collectstatic --noinput --settings=insightsvisualization.website.settings

echo ""
echo ">>> Step 6: Create superuser (if needed)"
echo "    Run manually if you haven't already:"
echo "    cd $SRC_DIR && python -m django createsuperuser --settings=insightsvisualization.website.settings"

echo ""
echo "============================================"
echo "  Setup Complete!"
echo "============================================"
echo ""
echo "PythonAnywhere Web App Configuration:"
echo "  Source code:    ${PROJECT_DIR}"
echo "  Working dir:    ${SRC_DIR}"
echo "  Virtualenv:     ${VENV_DIR}"
echo "  Static URL:     /static/"
echo "  Static dir:     ${PROJECT_DIR}/staticfiles"
echo "  Media URL:      /media/"
echo "  Media dir:      ${SRC_DIR}/insightsvisualization/media"
echo ""
echo "WSGI file: Copy contents of pythonanywhere_wsgi.py into"
echo "  /var/www/${PYTHONANYWHERE_USER}_pythonanywhere_com_wsgi.py"
echo ""
echo "Then reload your web app from the PythonAnywhere dashboard."
