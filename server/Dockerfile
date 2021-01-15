FROM python:3.9

COPY requirements.txt /tmp/

RUN pip3 install -r /tmp/requirements.txt

RUN useradd --create-home app

WORKDIR /home/app

RUN mkdir server

COPY server.py server

CMD ["python", "/home/app/server/server.py"]
