from websocket_ftx.client import FtxWebsocketClient
from time import sleep
from typing import DefaultDict, Deque, List, Dict, Tuple, Optional
import threading
from binance.client import Client as BinanceWebsocketClient
from binance.websockets import BinanceSocketManager
from datetime import datetime
import logging
import sys

from ftx.client import Client as Client_FTX
from binance.client import Client as Client_Binance

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])

class FtxSocketsHandler(FtxWebsocketClient):
    side = 'ask'
    def __init__(self, side) -> None:
        super().__init__()
        self.side = side

    def _handle_ticker_message(self, message: Dict) -> None:
        super()
        # print(message['data'][self.side])
        self.price = message['data'][self.side]

class BinanceSocketsHandler(BinanceWebsocketClient):    
    side = 'b'
    def __init__(self, side):
        super().__init__()
        self.side = side[0:1]

    def _handle_ticker_message(self, msg):
        self.price = float(msg['data'][self.side])
        

    def connect(self):
        self.sockets_manager = BinanceSocketManager(self)
        # self.ftx_socket = socket
    
    def get_ticker(self, symbol):
        self.symbol = symbol
        self.sockets_manager.start_symbol_ticker_futures_socket(symbol, self._handle_ticker_message)
        self.sockets_manager.start()



if __name__ == "__main__":
    # COINS HNT-PERP HNTUSDT
    # COINS RUNE-PERP RUNEUSDT
    direction = sys.argv[1]
    print(direction)

    if direction == 'open':
        ftx = FtxSocketsHandler('bid')
        binance = BinanceSocketsHandler('ask')
    else:
        ftx = FtxSocketsHandler('ask')
        binance = BinanceSocketsHandler('bid')

    ftx.connect()
    ftx.get_ticker('HNT-PERP')
    
    binance.connect()
    binance.get_ticker('HNTUSDT')

    while(True):
        try:
            print(
                f'{datetime.now()}, {(binance.price/ftx.price - 1) * 100},{binance.price},{ftx.price}', flush=True)
            sleep(10)
        except:
            pass
        # pass
