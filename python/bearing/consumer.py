# https://developer.confluent.io/get-started/python/#build-consumer

import numpy as np

from analysis import envelope_analysis
from detector import detection
from config import freqs

from confluent_kafka import Consumer

from prometheus_client import start_http_server, Counter, Histogram

if __name__ == '__main__':

    config = {
        # User-specific properties that you must set
        'bootstrap.servers': 'localhost:9094',
        'group.id': 'turbine-cms-consumer-3',
        'auto.offset.reset': 'earliest'
    }

    # Create Consumer instance
    consumer = Consumer(config)

    # Subscribe to topic
    topic = "features"
    consumer.subscribe([topic])

    start_http_server(8000)

    #messages_consumed = Counter('messages_consumed_total', 'Total messages consumed from Kafka')
    messages_consumed = Counter('messages_consumed_total', 'Total messages consumed', ['turbine_id'])
    faults_detected = Counter('faults_detected_total', 'Total faults detected', ['turbine_id'])
    #faults_detected = Counter('faults_detected_total', 'Total faults detected')
    processing_time = Histogram('message_processing_seconds', 'Time to process each message')

    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting...")
            elif msg.error():
                #print("ERROR: %s".format(msg.error()))
                print("ERROR: {}".format(msg.error()))
            else:
                print(f"Turbine: {msg.key().decode('utf-8')}")
                # Extract the (optional) key and value, and print.
                with processing_time.time():
                    signal = np.frombuffer(msg.value())
                    freqs_axis, mags, filt, env = envelope_analysis(signal, 20000)
                    half = len(freqs_axis) // 2
                    x = detection(freqs_axis[:half], mags[:half], freqs.BPFO, 29.95, 10)
                    turbine_id = msg.key().decode('utf-8')
                    messages_consumed.labels(turbine_id=turbine_id).inc()
                    faults_detected.labels(turbine_id=turbine_id).inc(len(x))
                    #messages_consumed.inc()
                    #faults_detected.inc(len(x))
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
