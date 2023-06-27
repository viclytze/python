'''
字典服务端tcp epoll版
'''
from socket import *
from select import *
import db_words
from interface import *


class TcpServer:
    '''
    基于套接字的TCP通信
    '''
    def __init__(self, addr):
        self.server = socket()
        self.server.bind(addr)
        self.server.listen(5)
        self.epoll = epoll()
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.map_ = {
            self.server.fileno(): self.server
        }
        self.epoll.register(self.server, EPOLLIN)
        self.db_words = db_words.WordsDBHandler()
        self.interface = Interface()

    def serve_for_ever(self):
        '''
        服务端入库
        :return:
        '''
        while True:
            events = self.epoll.poll()
            for fn, event in events:
                print(fn, event)
                if fn == self.server.fileno():
                    conn, addr = self.map_.get(fn).accept()
                    print('客户端连接: ', addr)
                    self.map_[conn.fileno()] = conn
                    self.epoll.register(conn, EPOLLIN | EPOLLERR)
                elif event & POLLERR:
                    self.close_client(fn)
                    continue
                elif event & POLLIN:
                    data = self.map_.get(fn).recv(4096)
                    print(data.decode())
                    if not data:
                        self.close_client(fn)
                        continue
                    res = self.interface.info_interface(data.decode())
                    if res:
                        self.map_[fn].send(res.encode())
                    else:
                        close(fn)

    def close_client(self, fn):
        '''
        关闭客户端连接
        :param fn: fileno
        '''
        print('客户端已关闭')
        self.epoll.unregister(fn)
        self.map_.get(fn).close()
        del self.map_[fn]


if __name__ == '__main__':
    addr = ('0.0.0.0', 8600)
    tcp_server = TcpServer(addr)
    tcp_server.serve_for_ever()
