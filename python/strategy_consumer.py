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


