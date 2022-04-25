# image app
FROM python:alpine3.15 as app


COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000


RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip freeze

COPY . /app
RUN ls -la
RUN export


CMD ["flask","run" ]


#image db
FROM mongo as db

EXPOSE 27017