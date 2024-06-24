#!/bin/bash
hiii
echo "BUILD START"

# Install Python dependencies from requirements.txt
python3.9 -m pip install -r requirements.txt

# Collect static files
python3.9 manage.py collectstatic --noinput --clear --directory staticfiles_build

echo "BUILD END"
