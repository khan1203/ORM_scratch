#!/bin/bash

# Exit on any error
set -e

DIRECTORY=".venv"

# Activate virtual environment
echo "🔌 Activating virtual environment"
source $DIRECTORY/bin/activate

# Check package integrity
twine check dist/*

# Upload package to pypi
twine upload dist/*