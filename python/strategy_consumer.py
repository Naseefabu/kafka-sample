from kafka import KafkaAdminClient, KafkaConsumer
from kafka import TopicPartition
from utils import get_orderbook_datafeed
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
            for msg in self.datafeed:
                print("consuming the market data from {} symbol {}".format(self.exchange,self.symbol))
                print(msg.value)
                self.datafeed.commit()


def main():
    mm_strategy = market_making(1,2,"kraken","AUD/JPY")
    p = multiprocessing.Process(target=mm_strategy.run)
    p.start()
    os.sched_setaffinity(p.pid, [0])
    p.join()


main()