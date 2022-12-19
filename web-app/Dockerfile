# syntax=docker/dockerfile:1

FROM --platform=linux/amd64 python:3.9.2  

WORKDIR /web-app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]