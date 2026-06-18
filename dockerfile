FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y dos2unix

RUN dos2unix start.sh

RUN chmod +x start.sh

CMD ["./start.sh"]