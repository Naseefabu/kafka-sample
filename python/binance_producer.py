from binance.websocket.spot.websocket_client import SpotWebsocketClient
from binance.spot import Spot as Client
from kafka.admin import KafkaAdminClient, NewTopic
from functools import partial
from kafka import KafkaProducer
import multiprocessing
import pandas as pd
import logging
import json
import time
import os


def json_serializer(data):
    return json.dumps(data).encode("utf-8")

#producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=json_serializer)

base_url = 'https://api.binance.com'
stream_url = 'wss://stream.binance.com:9443/ws'
client = Client(base_url=base_url)
ws_client = SpotWebsocketClient(stream_url=stream_url)
order_book = {
    "lastUpdateId": 0,
    "bids": [],
    "asks": []
}


def orderbook_message_handler(symbol,message,producer): 
    
    # print(symbol,symbols_dict[symbol])
    result = producer.send("binance-orderbook",message,partition=symbols_dict[symbol])
    print("result: ",result)

def listen_binance_orderbook(symbol):
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=json_serializer)
    ws_client.start()
    symbol = symbol.lower()
    ws_client.diff_book_depth(
        symbol=symbol.lower(),
        id=1,
        speed=1000,
        callback=lambda message: orderbook_message_handler(symbol, message, producer)
    )

def load_symbols():
    with open('binance_config.json') as f:
        data = json.load(f)
    symbol_dict = {symbol: number for symbol, number in data.items()}
    return symbol_dict

symbols_dict = load_symbols()

def main():

    global symbols_dict
    try:
        admin = KafkaAdminClient(bootstrap_servers='localhost:9092')

        topic = NewTopic(name='binance-orderbook',
                            num_partitions=len(symbols_dict),
                            replication_factor=1)
        admin.create_topics([topic])
    except Exception:
        pass
    symb = 'btcusdt'
    # listen_binance_orderbook(symb)
    processes = []
    for key, value in symbols_dict.items():
        # multiprocessing helps to bypass GIL 
        p = multiprocessing.Process(target=listen_binance_orderbook, args=(key,))
        processes.append(p)

    # start all processes
    for p in processes:
        p.start()

    # wait for all processes to complete
    for p in processes:
        p.join()


main()

#################

# # create an admin client instance
# admin_client = KafkaAdminClient(
#     bootstrap_servers=['localhost:9092'] # Kafka broker(s) connection string
# )

# # create a new topic
# try:
#     topic = NewTopic(
#         name='my_topic',
#         num_partitions=1,
#         replication_factor=1
#     )
#     admin_client.create_topics([topic])
# except Exception:
#     pass

# # create a KafkaProducer instance
# producer = KafkaProducer(
#     bootstrap_servers=['localhost:9092'], # Kafka broker(s) connection string
#     value_serializer=lambda v: json.dumps(v).encode('utf-8') # serialize messages as JSON
# )

# # send events
# while True:
#     event1 = {'event_type': 'user_created', 'user_id': 1234, 'timestamp': '2023-04-20T10:00:00Z'}
#     producer.send('my_topic', event1)

#     event2 = {'event_type': 'user_updated', 'user_id': 1234, 'timestamp': '2023-04-20T11:00:00Z'}
#     producer.send('my_topic', event2)



