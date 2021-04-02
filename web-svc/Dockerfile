FROM python:3.7.5

ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /web
COPY requirements.txt /web
WORKDIR /web

RUN pip install --upgrade pip && pip install -r requirements.txt
