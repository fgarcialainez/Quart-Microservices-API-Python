FROM python:3.10.5-bullseye

ENV PYTHONPATH /app/src/
ENV QUART_APP app:app

WORKDIR /app

COPY . /app

RUN pip install -r /app/requirements.txt

CMD hypercorn --workers $WORKERS --bind 0.0.0.0:$PORT app:app
