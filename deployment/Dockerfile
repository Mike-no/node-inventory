FROM python:3.8-slim-buster

RUN apt-get update -y && apt-get install -y python3-pip

WORKDIR /k8s-node-inventory

COPY api/ api/
COPY db/ db/
COPY app.py app.py

COPY deployment/config/config.ini config.ini
COPY requirements.txt requirements.txt

VOLUME k8s-node-inventory

RUN pip3 install -r requirements.txt

CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
