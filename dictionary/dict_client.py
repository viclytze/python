'''
词典客户端
'''
import socket
import hashlib
import sys


def pwd_hash(password):
    obj = hashlib.md5()
    obj.update(password.encode('utf8'))
    return obj.hexdigest()


def main_view():
    client = socket.socket()
    client.connect(('192.168.50.100', 8600))

    while True:
        print('''
                ======================================
                =============   无道词典  =============
                ======================================
                              1  注册
                              2  登入
                              3  退出   
                ====================================== 
        ''')
        choise = input('请选择: ').strip()
        if choise == '3':
            client.send(b'Q QUIT')
            client.close()
            sys.exit()
        elif choise == '1':
            res = register()
            client.send(res.encode())
        elif choise == '2':
            res = login()
            client.send(res.encode())
        else:
            print('输入有误请重新输入')
            continue
        flag, msg = client.recv(4096).decode().split(' ',1)
        if flag == 'OK':
            print(msg)
            consult_view(client)
        else:
            print(msg)


def register():
    while True:
        user = input('请输入用户名: ').strip()
        if user.lower() == 'q':
            return
        password = input('请输入密码: ').strip()
        re_pwd = input('请在次输入密码: ').strip()
        if password != re_pwd or not password:
            print('密码错误')
            continue
        else:
            password = pwd_hash(password)
            msg = 'R {} {}'.format(user, password)
            return msg


def login():
    user = input('请输入用户名: ').strip()
    if user.lower() == 'q':
        return
    password = input('请输入密码: ').strip()
    if not password:
        print('密码错误')
        return
    else:
        password = pwd_hash(password)
        msg = 'L {} {}'.format(user, password)
        return msg


def consult_view(client):
    while True:
        print('''
                ======================================
                =============   无道词典  =============
                ======================================
                              1  查询单词
                              2  查询历史
                              3  退出   
                ====================================== 
        ''')
        choise = input('请选择: ').strip()
        if choise == '3':
            client.send(b'Q QUIT')
            client.close()
            sys.exit()
        elif choise == '1':
            res = input('请输入单词: ').strip()
            res = 'S {}'.format(res)
            client.send(res.encode())
        elif choise == '2':
            res = 'H History'
            client.send(res.encode())
        else:
            print('输入有误请重新输入')
            continue
        flag, msg = client.recv(4096).decode().split(' ',1)
        print(msg)


if __name__ == '__main__':
    main_view()
