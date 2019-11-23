FROM python:3

COPY main.py requirements.txt /app/

WORKDIR /app/

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3", "./main.py" ]
