FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install numpy scipy matplotlib pytest confluent-kafka prometheus-client psycopg2-binary

CMD ["python", "consumer.py"]
