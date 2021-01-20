from binance.client import Client as binance_client
from binance.websockets import BinanceSocketManager

binance = binance_client()


def process_message(msg):
    print("message type: {}".format(msg['e']))
    print(msg)
    # do something


bm = BinanceSocketManager(binance)
# start any sockets here, i.e a trade socket
conn_key = bm.start_symbol_ticker_socket('BNBBTC', process_message)
# then start the socket manager
bm.start()
