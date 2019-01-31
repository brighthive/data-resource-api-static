FROM python:3.7.2-slim
WORKDIR /tpot-programs/api
ADD api api
ADD config config
ADD db db
ADD schema schema
ADD app.py app.py
ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock
