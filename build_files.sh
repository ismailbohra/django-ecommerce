#!/bin/bash

echo "BUILD START"

# Ensure staticfiles_build directory exists
mkdir -p staticfiles_build

# Install Python dependencies from requirements.txt
/usr/bin/python3.9 -m pip install -r requirements.txt

# Collect static files
/usr/bin/python3.9 manage.py collectstatic --noinput --clear --directory staticfiles_build

echo "BUILD END"
