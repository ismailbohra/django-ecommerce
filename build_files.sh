#!/bin/bash

echo "BUILD START"

# Install Python dependencies from requirements.txt
pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic

echo "BUILD END"
