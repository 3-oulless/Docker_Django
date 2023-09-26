FROM python:3.8-slim-buster


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app



RUN pip install --upgrade pip 
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./Django_E /app/


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]