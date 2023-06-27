'''
服务端入库
'''
# from core import *
from core_gevent import *



if __name__ == '__main__':
    addr = ('0.0.0.0', 8600)
    tcp_server = TcpServer(addr)
    tcp_server.serve_for_ever()
