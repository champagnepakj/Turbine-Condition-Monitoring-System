# https://developer.confluent.io/get-started/python/#build-consumer

import numpy as np

from analysis import envelope_analysis
from detector import detection
from config import freqs

from confluent_kafka import Consumer

if __name__ == '__main__':

    config = {
        # User-specific properties that you must set
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'turbine-cms-consumer-2',
        'auto.offset.reset': 'earliest'
    }

    # Create Consumer instance
    consumer = Consumer(config)

    # Subscribe to topic
    topic = "features"
    consumer.subscribe([topic])

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
                # Extract the (optional) key and value, and print.
                signal = np.frombuffer(msg.value())
                freqs_axis, mags, filt, env = envelope_analysis(signal, 20000)
                half = len(freqs_axis) // 2
                detection(freqs_axis[:half], mags[:half], freqs.BPFO, 29.95, 10)
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
