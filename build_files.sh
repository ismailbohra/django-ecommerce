echo "BUILD START"

mkdir -p staticfiles_build


python3.9 -m pip install -r requirements.txt

# Collect static files
python3.11 manage.py collectstatic --noinput --clear

echo "BUILD END"