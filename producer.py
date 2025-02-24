import json
import requests
from sseclient import SSEClient
from confluent_kafka import Producer

# Kafka configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'wiki-producer'
}

# Create Producer instance
producer = Producer(**conf)

# Wikipedia Recent Changes SSE endpoint
WIKIPEDIA_URL = 'https://stream.wikimedia.org/v2/stream/recentchange'

def delivery_report(err, msg):
    if err is not None:
        print(f'Delivery failed for record {msg.key()}: {err}')
    else:
        print(f'Record {msg.key()} successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')

def produce_to_kafka(event_data):
    try:
        # Send the message to Kafka
        producer.produce(topic='wikipedia-test', value=json.dumps(event_data), callback=delivery_report)
        producer.poll(0)
    except Exception as e:
        print(f'Failed to produce message: {e}')

def main():
    # Connect to the Wikipedia SSE stream
    s = requests.Session()

    with s.get(WIKIPEDIA_URL, headers=None, stream=True) as resp:
        for line in resp.iter_lines():
            try:
                event_data = json.loads(line)
                print(f'New event: {event_data}')
                produce_to_kafka(event_data)
            except json.JSONDecodeError as e:
                print(f'Failed to decode JSON: {e}')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Stopped by user.')
    finally:
        producer.flush()
