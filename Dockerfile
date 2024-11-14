FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

RUN rm /app/CareerCloset/settings.py
RUN mv /app/CareerCloset/settings-prod.py /app/CareerCloset/settings.py

RUN python manage.py collectstatic --noinput

RUN pip install gunicorn

CMD ["sh", "-c", "python manage.py migrate &&  python manage.py create_groups && gunicorn --bind 0.0.0.0:8000 CareerCloset.wsgi:application"]