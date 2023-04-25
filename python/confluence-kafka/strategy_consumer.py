
from utils import get_orderbook_datafeed
from confluent_kafka import Consumer, KafkaError
import multiprocessing
import json
import os


class market_making:
    def __init__(self, bidspread, askspread, exchange, symbol):
        print("starting the strategy")
        # symbols it listening to
        self.symbol = symbol # symbol its market making
        self.exchange = exchange # exchange its market making
        self.bid_spread = bidspread
        self.ask_spread = askspread
        self.datafeed = get_orderbook_datafeed(exchange,symbol) # returns kafka consumer object 

    def run(self):
        while True:
            msg = self.datafeed.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print('Reached end of partition')
                else:
                    print(f'Error while consuming message: {msg.error()}')
            else:
                print(f'Received message: {msg.value()}')

            # Manually commit the offset after processing the message
            self.datafeed.commit()


def main():
    mm_strategy = market_making(1,2,"kraken","AUD/JPY")
    p = multiprocessing.Process(target=mm_strategy.run)
    p.start()
    os.sched_setaffinity(p.pid, [0])
    p.join()


main()