FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app

CMD [ "python", "main.py"]


