
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
>>>>>>> a90443b (Add build.sh and data.json)
>>>>>>> c220dea
python manage.py loaddata data.json