import pymysql
try:
    import db_config
    BD_CONFIG = db_config.DB_CONFIG
except ImportError:
    DB_CONFIG = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "passwd": "",
        "db": "summer",
        "charset": "utf8"
    }


class SQLManager(object):

    # 初始化实例方法
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    # 连接数据库
    def connect(self):
        self.conn = pymysql.connect(
            host=db_config.DB_CONFIG["host"],
            port=db_config.DB_CONFIG["port"],
            user=db_config.DB_CONFIG["user"],
            passwd=db_config.DB_CONFIG["passwd"],
            db=db_config.DB_CONFIG["db"],
            charset=db_config.DB_CONFIG["charset"]
        )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 查询多条数据
    def get_list(self, sql, args=None):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    # 查询单条数据
    def get_one(self, sql, args=None):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    # 执行单条SQL语句
    def moddify(self, sql, args=None):
        self.cursor.execute(sql, args)
        self.conn.commit()

    # 我如果要批量执行多个创建操作，虽然只建立了一次数据库连接但是还是会多次提交，可不可以改成一次连接，
    # 一次提交呢？
    # 可以，只需要用上pymysql的executemany()
    # 方法就可以了。
    # 执行多条SQL语句
    def multi_modify(self, sql, args=None):
        self.cursor.executemany(sql, args)
        self.conn.commit()

    # 创建单条记录的语句
    def create(self, sql, args=None):
        self.cursor.execute(sql, args)
        self.conn.commit()
        last_id = self.cursor.lastrowid
        return last_id

    # 关闭数据库cursor和连接
    def close(self):
        self.cursor.close()
        self.conn.close()

    def __enter__(self):
        return self

    # 退出with语句块自动执行
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
