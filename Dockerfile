FROM python:3.8

WORKDIR /opt/hospitalite

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .