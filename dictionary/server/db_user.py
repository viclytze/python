import pymysql


class DBUser():
    '''
    用户数据类
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


    def register(self, user, password):
        '''
        用户注册
        :param user: 用户名
        :param password: 密码
        :return:
        '''
        sql = "select * from user where user.user=%s"
        try:
            res = self.cur.execute(sql, user)
            if res:
                return 'NO 用户已存在'
            else:
                sql = "insert into user values (%s,%s)"
                try:
                    self.cur.execute(sql, [user, password])
                    self.db.commit()
                    return 'OK 注册成功'
                except Exception as e:
                    print(e)
                    self.db.rollback()
                    return 'NO {}'.format(e)
        except Exception as e:
            print(e)
            self.db.rollback()
            return 'NO {}'.format(e)

    def login(self, user, password):
        '''
        登入验证
        :param user: 用户名
        :param password: 密码
        :return:
        '''
        sql = "select * from user where user.user=%s"
        try:
            self.cur.execute(sql, user)
            res = self.cur.fetchone()
            if (user, password) == res:
                return 'OK 登入成功'
            else:
                return 'NO 用户名密码错误'
        except Exception as e:
            print(e)
            self.db.rollback()
            return 'NO {}'.format(e)