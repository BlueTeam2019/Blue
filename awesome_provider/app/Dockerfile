FROM python:3

WORKDIR /app
COPY . /app

RUN python3 -m pip install --no-cache-dir -r requierments.txt

CMD  python3 src/routing.py