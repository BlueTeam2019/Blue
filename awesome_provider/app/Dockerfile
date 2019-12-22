FROM python:3

WORKDIR /app
COPY . /app

RUN ls
RUN pip install --no-cache-dir -r requierments.txt

CMD  python3 provider_routing.py ${DB_URL} ${DB_USR} ${DB_PASS} ${DB_NAME}