FROM python:3-slim

WORKDIR /app
COPY . /app

RUN python3 -m pip install --no-cache-dir -r requirements.txt
RUN chmod 777 /app/in

CMD  python3 src/routing.py