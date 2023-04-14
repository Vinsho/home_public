FROM python:3.11
EXPOSE 8000

RUN apt-get update && apt-get install -y libpq-dev && apt-get install -y cron
RUN pip3 install --upgrade pip

WORKDIR /home 
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY . .

RUN env >> /etc/environment

RUN python manage.py makemigrations 
RUN python manage.py migrate
RUN python manage.py collectstatic --no-input

RUN chmod +x /home/entry.sh
RUN touch /home/job.log

ENTRYPOINT ["/home/entry.sh"]
CMD ["gunicorn", "home.wsgi:application", "--bind", "0.0.0.0:8000"]
