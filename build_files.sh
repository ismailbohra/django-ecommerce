#!/bin/bash

echo "BUILD START"

# Install Python dependencies from requirements.txt
python3 -m pip install -r requirements.txt

mkdir -p staticfiles_build

# Collect static files
python3 manage.py collectstatic --noinput --clear --directory staticfiles_build

echo "BUILD END"
