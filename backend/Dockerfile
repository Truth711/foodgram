FROM python:3.10.6-slim

RUN mkdir /app

COPY requirements.txt /app

RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt --no-cache-dir

COPY . /app

WORKDIR /app

CMD ["gunicorn", "foodgram_project.wsgi:application", "--bind", "0:8000" ]
