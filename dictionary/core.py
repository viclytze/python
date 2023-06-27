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
            print('register:', self.map_)
            events = self.epoll.poll()
            for fn, event in events:
                print(fn, event)
                if fn == self.server.fileno():
                    conn, addr = self.map_.get(fn).accept()
                    print('客户端连接: ', addr)
                    self.map_[conn.fileno()] = conn
                    self.epoll.register(conn, EPOLLIN | EPOLLERR)
                elif event & POLLERR:
                    print('客户端已关闭')
                    self.epoll.unregister(fn)
                    self.map_.get(fn).close()
                    del self.map_[fn]
                    continue
                elif event & POLLIN:
                    data = self.map_.get(fn).recv(4096)
                    print(data.decode())
                    if not data:
                        print('客户端已关闭')
                        self.epoll.unregister(fn)
                        self.map_.get(fn).close()
                        del self.map_[fn]
                        continue
                    self.map_[fn].send(b'ok')



if __name__ == '__main__':
    addr = ('0.0.0.0', 8600)
    tcp_server = TcpsServer(addr)
    tcp_server.main()
