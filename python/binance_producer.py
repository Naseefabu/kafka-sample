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

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=json_serializer)

base_url = 'https://api.binance.com'
stream_url = 'wss://stream.binance.com:9443/ws'
client = Client(base_url=base_url)
ws_client = SpotWebsocketClient(stream_url=stream_url)
order_book = {
    "lastUpdateId": 0,
    "bids": [],
    "asks": []
}


def orderbook_message_handler(symbol,message): 
    
    print(symbol,symbols_dict[symbol])
    producer.send("binance-orderbook",message,partition=symbols_dict[symbol])


def listen_binance_orderbook(symbol):
    ws_client.start()
    symbol = symbol.lower()
    ws_client.diff_book_depth(
        symbol=symbol.lower(),
        id=1,
        speed=1000,
        callback=lambda message: orderbook_message_handler(symbol, message)
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
