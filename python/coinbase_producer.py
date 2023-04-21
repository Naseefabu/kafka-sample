import ccxt.pro
import ccxt
import json
import asyncio
import multiprocessing as mp
from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaProducer

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

async def subscribe_orderbook(symbol,symbols_partition_map):
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=json_serializer)
    exchange = ccxt.pro.coinbasepro({
        'enableRateLimit': True,
        'rateLimit': 1000
    })
    while True:
        snapshot = await exchange.watch_order_book(symbol,5)
        result = producer.send("coinbase-orderbook",snapshot,partition=symbols_partition_map[symbol])
        print(snapshot)

def run_coinbase_feed(symbols_partition_map):

    try:
        admin = KafkaAdminClient(bootstrap_servers='localhost:9092')

        topic = NewTopic(name='coinbase-orderbook',
                            num_partitions=len(symbols_partition_map),
                            replication_factor=1)
        admin.create_topics([topic])
    except Exception:
        pass

    processes = []
    for symbol in symbols_partition_map.keys():
        p = mp.Process(target=asyncio.run, args=(subscribe_orderbook(symbol,symbols_partition_map),))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


def load_symbols_partition_map():
    with open('coinbase_config.json') as f:
        data = json.load(f)
    symbol_dict = {symbol: number for symbol, number in data.items()}
    return symbol_dict

# symbols to subscribe
symbols = load_symbols_partition_map()
run_coinbase_feed(symbols)

# exchange = ccxt.coinbasepro()
# markets = exchange.load_markets()

# print(markets.keys())

