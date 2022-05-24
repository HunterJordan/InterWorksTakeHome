FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas==1.3.5 numpy sqlalchemy psycopg2

WORKDIR /usr/
COPY app/. ./app
COPY main.py main.py


CMD ls -la /
EXPOSE 5005

ENTRYPOINT [ "python", "-u", "main.py" ]