FROM python:3.7-alpine as alpyn

FROM alpyn as pilder
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip3 install --install-option="--prefix=/install" -r /requirements.txt

FROM alpyn
COPY --from=pilder /install /usr/local
COPY . /app

WORKDIR /app

# VOLUME [ "/log" ]

ENTRYPOINT ["python"] 
CMD ["app.py"]