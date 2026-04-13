#!/bin/bash

# Exit on any error
set -e

DIRECTORY=".venv"
APP_MODULE="core"

# Activate virtual environment
echo "🔌 Activating virtual environment"
source $DIRECTORY/bin/activate

# Show Python version and location
echo "🐍 Python version and location:"
which python3
python3 --version

# format gunicorn {root_module}.{main_python_file_name}:{app_variable_name}
gunicorn "$APP_MODULE".main:app --reload --bind=localhost:8000

# gunicorn core.main:app --reload --bind=localhost:8000       
fuser -k 8000/tcp || true && gunicorn core.main:app --reload --bind=localhost:8000