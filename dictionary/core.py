from socket import *
from select import *


class TcpsServer:
    def __init__(self, addr):
        self.server = socket()
        self.server.bind(addr)
        self.server.listen(5)
        self.epoll = epoll()
        self.map_ = {
            self.server.fileno(): self.server
        }
        self.epoll.register(self.server, EPOLLIN)

    def main(self):
        while True:
            events = self.epoll.poll()
            for fn, event in events:
                if fn == self.server.fileno():
                    conn, addr = self.map_.get(fn).accept()
                    self.map_[conn.fileno()] = conn
                    self.epoll.register(conn,EPOLLIN)
                elif event & POLLIN:
                    data = self.map_.get(fn).recv(4096)
                    if not data:
                        print('客户端已关闭')
                        self.map_[fn].close()
                        self.epoll.unregister(fn)
                        del self.map_[fn]
                        continue
                    self.map_[fn].send(b'ok')


if __name__ == '__main__':
    addr = ('0.0.0.0',8600)
    tcp_server = TcpsServer(addr)
    tcp_server.main()