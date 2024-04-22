# syntax=docker/dockerfile:1
FROM python:3.10-alpine
WORKDIR /the-real-master-app
ENV BOT_APP=main.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python3", "main.py"] 