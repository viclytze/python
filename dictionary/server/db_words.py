'''
字典数据库
'''
import pymysql


class WordsDBHandler:
    '''
    字典查询类
    '''
    def __init__(self):
        self.host = '192.168.50.100'
        self.port = 3306
        self.user = 'root'
        self.passwd = '123456'
        self.charset = 'utf8'
        self.database = 'dict'
        self.db = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            charset=self.charset,
            database=self.database
        )
        self.cur = self.db.cursor()
        self.history_list = []

    def save_word(self, word, explain):
        '''
        后台导入数据库用
        :param word: 单词
        :param explain: 解释
        '''
        sql = "INSERT INTO words (words.word,words.mean) VALUES (%s,%s)"
        try:
            self.cur.execute(sql, [word, explain])
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

    def select_word(self, word):
        '''
        单词查询
        :param word: 单词
        :return: 返回给客户端的数据(经过封装)
        '''
        print(word)
        sql = "select words.mean from words where word=%s"
        try:
            self.cur.execute(sql, word)
            res = self.cur.fetchall()[0][0]
            self.history_list.append(word)
            return 'OK {}'.format(res)
        except Exception :
            return 'NO 单词没找到'

    def history(self, msg):
        '''
        查看用户查询历史,默认最后10条,为零时数据
        :param msg: 无用参数
        :return: 返回给客户端的数据(经过封装)
        '''
        if len(self.history_list) >= 10:
            msg = '\n'.join(self.history_list[-1:-11:-1])
            return 'OK {}'.format(msg)
        else:
            msg = '\n'.join(self.history_list[::-1])
            return 'OK {}'.format(msg)


if __name__ == '__main__':
    db = WordsDBHandler()
    # with open('dict2.txt', mode='rt', encoding='utf-8') as f:
    #     for line in f:
    #         index, msg = line.strip().split('##')
    #         db.save_word(index,msg)

    res = db.select_word('dasd')
    print(res)
