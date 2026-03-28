#!/bin/bash

# Exit on any error
set -e

DIRECTORY=".venv"

# Activate virtual environment
echo "🔌 Activating virtual environment"
source $DIRECTORY/bin/activate

python setup.py sdist bdist_wheel

# Check package integrity
echo "🔌 Verify dist using twine"
twine check dist/*