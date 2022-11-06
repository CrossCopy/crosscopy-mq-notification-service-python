FROM python:3.9.10-buster

COPY . /notification
WORKDIR /notification
RUN pip install -r requirements.txt
CMD ["stdbuf", "-oL", "python", "-u", "main.py"]