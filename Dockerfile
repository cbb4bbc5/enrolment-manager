FROM python:3.12

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV TZ="Europe/Warsaw"

COPY requirements.txt .
RUN pip install -r requirements.txt
