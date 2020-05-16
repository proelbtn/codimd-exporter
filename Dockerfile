FROM python:3.8

RUN apt install unzip

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["bash", "./scripts/entrypoint.sh"]
