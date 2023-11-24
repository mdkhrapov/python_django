FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app_log

COPY logging/requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY logging/mysite/ .

CMD ["python", "manage.py", "runserver"]