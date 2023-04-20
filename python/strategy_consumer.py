from kafka import KafkaAdminClient, KafkaConsumer
from kafka import TopicPartition
import json

consumer = KafkaConsumer(              
    bootstrap_servers=['localhost:9092'],
    group_id="strategy-three",           
    auto_offset_reset='earliest',  

)

# assign to a specific partition of the topic
partition = TopicPartition('binance-orderbook', 1)
consumer.assign([partition])

# seek to the beginning of the partition
consumer.seek_to_beginning(partition)

while True:
    for msg in consumer:
        print("inside")
        print("binance orderbook = {}".format(json.loads(msg.value)))



#################

# consumer = KafkaConsumer(
#     'my_topic',                    # topic name
#     bootstrap_servers=['localhost:9092'], # Kafka broker(s) connection string
#     group_id='my_group',           # consumer group ID
#     auto_offset_reset='earliest',  # earliest offset available
#     enable_auto_commit=True,       # commit offsets automatically
#     value_deserializer=lambda x: json.loads(x.decode('utf-8')) # deserialize message value as JSON
# )

# # consume events
# for message in consumer:
#     event = message.value
#     print(f"Received {event['event_type']} event for user {event['user_id']} at {event['timestamp']}")