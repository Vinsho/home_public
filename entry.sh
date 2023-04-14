#!/bin/sh
service cron start

python manage.py crontab add
python manage.py crontab show

exec "$@"
