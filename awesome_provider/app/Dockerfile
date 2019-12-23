FROM python:3

WORKDIR /app
COPY . /app

RUN apt-get install python3-pymysql
RUN python3 -m pip install --no-cache-dir -r requierments.txt
CMD  python3 src/provider_routing.py ${DB_URL} ${DB_USR} ${DB_PASS} ${DB_NAME} ${DB_PORT}