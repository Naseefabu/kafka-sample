from kafka import KafkaAdminClient, KafkaConsumer
from kafka import TopicPartition
import json



class market_making:
    def __init__(self, bidspread, askspread, symbols):
        # symbols it listening to
        self.symbols = symbols
        self.bid_spread = bidspread
        self.ask_spread = askspread
        self.consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                                 group_id='strategy-marketmaking',
                                 auto_offset_reset='earliest'
                                 )
    def run_strategy(self):
            
        while True:
            for msg in self.consumer:
                print(msg)





def test():
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

    for msg in consumer:
        print("binance orderbook = {}".format(json.loads(msg.value)))
