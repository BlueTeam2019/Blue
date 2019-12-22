FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install git+git://github.com/bloomberg/python-github-webhook.git
RUN pip install --no-cache-dir -r requirements.txt
RUN export FLASK_APP=app.py

EXPOSE 5000

COPY . .

CMD flask run --host=0.0.0.0