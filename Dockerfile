# start by pulling the python image
FROM python:alpine3.15

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000

# install the dependencies and packages in the requirements file
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip freeze

# copy every content from the local file to the image
COPY . /app
RUN ls -la
RUN export

# configure the container to run in an executed manner
#ENTRYPOINT [ "flask" ]

CMD ["flask","run" ]