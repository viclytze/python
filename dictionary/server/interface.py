'''

'''
from db_words import *
from db_user import *


class Interface:
    '''
    接收信息逻辑处理
    '''
    def __init__(self):
        self.consult = WordsDBHandler()
        self.db_user = DBUser()
        self.choise_dict = {
            'Q': self.logout,
            'R': self.register,
            'L': self.login,
            'S': self.consult.select_word,
            'H': self.consult.history
        }

    def info_interface(self, msg):
        '''
        接收信息逻辑处理
        :param msg: 客户端发送的数据
        :return: 返回给客户端的数据(经过封装)
        '''
        tmp_list = msg.split(' ', 1)
        if tmp_list[0] in self.choise_dict:
            res = self.choise_dict.get(tmp_list[0])(tmp_list[1])
            return res
        else:
            return 'NO error'

    def logout(self, msg):
        return False

    def register(self, msg):
        '''
        注册接口,处理数据后提交DB
        :param msg: 客户端发送的数据(去头)
        :return: 返回给客户端的数据(经过封装)
        '''
        tmp_list = msg.split(' ', 1)
        user = tmp_list[0]
        password = tmp_list[1]
        print(user, password)
        return self.db_user.register(user, password)

    def login(self, msg):
        '''
        注册接口,处理数据后提交DB
        :param msg: 客户端发送的数据(去头)
        :return: 返回给客户端的数据(经过封装)
        '''
        tmp_list = msg.split(' ', 1)
        user = tmp_list[0]
        password = tmp_list[1]
        print(user, password)
        return self.db_user.login(user, password)


if __name__ == '__main__':
    msg = 'Q quit'
    itf = Interface()
    itf.info_interface(msg)
