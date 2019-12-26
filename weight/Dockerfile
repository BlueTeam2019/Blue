FROM python:3.7.2-slim

COPY . /app

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --upgrade -r requirements_web.txt

ENTRYPOINT ["python"]
CMD ["app.py"]