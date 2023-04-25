from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer
import multiprocessing as mp
import asyncio
import json
import os
import ccxt
import ccxt.pro


async def subscribe_orderbook(symbol, symbols_partition_map):
    producer = Producer({"bootstrap.servers": "localhost:9092"})
    exchange = ccxt.pro.bybit({"enableRateLimit": True, "rateLimit": 1000})
    while True:
        snapshot = await exchange.watch_order_book(symbol)
        producer.produce(
            topic="bybit-orderbook",
            key=None,
            value=json.dumps(snapshot).encode("utf-8"),
            partition=symbols_partition_map[symbol],
        )
        # Wait for any outstanding messages to be delivered to kafka broker
        producer.flush()
        print(snapshot)


def run_binance_feed(symbols_partition_map):
    try:
        admin = AdminClient({"bootstrap.servers": "localhost:9092"})

        topic = NewTopic(
            "bybit-orderbook",
            num_partitions=len(symbols_partition_map),
            replication_factor=1
        )
        admin.create_topics([topic])
    except Exception:
        pass

    num_cores = mp.cpu_count()
    processes = []
    symbols = list(symbols_partition_map.keys())
    for i in range(num_cores):
        symbols_per_process = symbols[i::num_cores]
        if not symbols_per_process: # if number of cores greater than number of symbols
            continue
        p = mp.Process(
            target=run_event_loop,
            args=(
                symbols_per_process,
                symbols_partition_map,
            ),
        )
        processes.append(p)
        p.start()
        os.sched_setaffinity(p.pid, [i])

    for p in processes:
        p.join()


def run_event_loop(symbols, symbols_partition_map):
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    for symbol in symbols:
        loop.create_task(subscribe_orderbook(symbol, symbols_partition_map))
    loop.run_forever()


def load_symbols_partition_map():
    with open("bybit_config.json") as f:
        data = json.load(f)
    symbol_dict = {symbol: number for symbol, number in data.items()}
    return symbol_dict


# symbols to subscribe
symbols = load_symbols_partition_map()
run_binance_feed(symbols)