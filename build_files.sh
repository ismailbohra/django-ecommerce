#!/bin/bash

echo "BUILD START"

# Ensure staticfiles_build directory exists
mkdir -p staticfiles_build

# Install Python dependencies from requirements.txt
python3 -m pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput --clear --directory staticfiles_build

echo "BUILD END"
