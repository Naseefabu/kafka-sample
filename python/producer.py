from kafka import KafkaProducer, KafkaConsumer
import json

# Configure Kafka producer
bootstrap_servers = 'localhost:9092'  # Update with your Kafka bootstrap servers
producer_topic = 'event_topic'  # Update with the desired Kafka topic for producer

producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Produce events to Kafka topic
events = [{'event_id': 1, 'event_name': 'Event1'},
          {'event_id': 2, 'event_name': 'Event2'},
          {'event_id': 3, 'event_name': 'Event3'}]

for event in events:
    producer.send(producer_topic, value=event)
    print("Produced event: ", event)

# Configure Kafka consumer
consumer_topic = 'event_topic'  # Update with the Kafka topic used by the producer
consumer = KafkaConsumer(consumer_topic, bootstrap_servers=bootstrap_servers,
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')))

# Consume events from Kafka topic
for message in consumer:
    event = message.value
    print("Consumed event: ", event)