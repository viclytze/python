'''
电子辞典服务端tcp gevent版
'''
import gevent
from gevent import monkey

monkey.patch_all()
from socket import *

import db_words
from interface import *


class TcpServer:
    def __init__(self, addr):
        self.server = socket()
        self.server.bind(addr)
        self.server.listen(5)
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.map_ = {
            self.server.fileno(): self.server
        }
        self.db_words = db_words.WordsDBHandler()
        self.interface = Interface()

    def serve_for_ever(self):
        while True:
            conn, addr = self.server.accept()
            print('客户端连接: ', addr)
            g = gevent.spawn(self.reguest, conn)

    def reguest(self, conn):
        while True:
            data = conn.recv(4096)
            if not data:
                conn.close()
                return
            res = self.interface.info_interface(data.decode())
            if res:
                conn.send(res.encode())
            else:
                conn.close()
                return


if __name__ == '__main__':
    addr = ('0.0.0.0', 8600)
    tcp_server = TcpServer(addr)
    tcp_server.serve_for_ever()
