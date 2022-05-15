# init a base image 
FROM python:3.9-slim-buster
# define the present working directory
WORKDIR /cbr-front
# copy the contents into the working dir
ADD . /cbr-front
# run pip to install the dependencies of the flask app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
# define the command to start the container
CMD ["python3","apptest1.py"]
