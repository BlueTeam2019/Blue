FROM python:latest

COPY . /app

WORKDIR /app

RUN pip install --upgrade -r requirements_web.txt
ENTRYPOINT ["python"]

CMD ["app.py"]