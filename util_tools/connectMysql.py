import pymysql
from util_tools.logs_util.recordlog import logs
from util_tools.handle_data.configParse import ConfigParse

conf = ConfigParse()


class ConnectMysql:
    def __init__(self):
        self.conf = {
            'host': conf.get_section_mysql('host'),
            'port': int(conf.get_section_mysql('port')),
            'user': conf.get_section_mysql('user'),
            'password': conf.get_section_mysql('password'),
            'database': conf.get_section_mysql('database')
        }
        self.conn = None
        self.cursor = None
        try:
            self.conn = pymysql.connect(**self.conf)
            # 获取操作游标，DictCursor 让结果以字典形式返回
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            logs.info(f'连接数据库成功，数据库ip为：{self.conf.get("host")}')
        except Exception as e:
            logs.error(f'连接数据库失败：{e}')
            raise

    def close(self):
        """关闭数据库连接"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            logs.info('数据库连接已关闭')
        except Exception as e:
            logs.error(f'关闭数据库连接失败：{e}')

    def query(self, sql, fetchone=False):
        """
        查询数据库数据
        :param sql: 查询的SQL语句
        :param fetchone: True 返回单条，False 返回全部
        :return: 查询结果
        """
        try:
            self.cursor.execute(sql)
            if fetchone:
                return self.cursor.fetchone()
            return self.cursor.fetchall()
        except Exception as e:
            logs.error(f'查询数据库数据失败：{e}')
            raise

    def delete(self, table, condition, must_affect=True):
        """
        删除数据库数据（先查有没有，有才删）
        :param table: 表名，如 'ecs_users'
        :param condition: where 条件，如 "user_name = 'lisi1234'"
        :param must_affect: True 时删 0 行报错；False 时删 0 行只记日志
        :return: 受影响行数
        """
        try:
            # 1. 先查有没有
            self.cursor.execute(f"select * from {table} where {condition}")
            if not self.cursor.fetchall():
                logs.info(f'数据不存在，跳过删除：{table} where {condition}')
                return 0

            # 2. 有才删
            rows = self.cursor.execute(f"delete from {table} where {condition}")
            self.conn.commit()

            if must_affect and rows == 0:
                logs.error(f'删除失败，未匹配到任何数据：{table} where {condition}')
                raise AssertionError('删除影响行数为 0')

            logs.info(f'删除数据库数据成功，受影响行数：{rows}')
            return rows
        except AssertionError:
            raise
        except Exception as e:
            logs.error(f'删除数据库数据失败：{e}')
            raise

    def update(self, sql, table=None, condition=None):
        """
        更新数据库数据（传了 table 和 condition 时会先查存在）
        :param sql: 更新的SQL语句
        :param table: 表名，如 'ecs_users'（可选）
        :param condition: 存在条件，如 "user_name = 'lisi1234'"（可选）
        :return: 受影响行数
        """
        try:
            # 如果传了检查条件，先查在不在
            if table and condition:
                self.cursor.execute(f"select * from {table} where {condition}")
                if not self.cursor.fetchall():
                    logs.info(f'数据不存在，跳过更新：{table} where {condition}')
                    return 0

            rows = self.cursor.execute(sql)
            self.conn.commit()
            logs.info(f'更新数据库数据成功，受影响行数：{rows}')
            return rows
        except Exception as e:
            logs.error(f'更新数据库数据失败：{e}')
            raise

    def insert(self, sql, table=None, condition=None):
        """
        插入数据库数据（传了 table 和 condition 时会先查重）
        :param sql: 插入的SQL语句
        :param table: 表名，如 'ecs_users'（可选）
        :param condition: 查重条件，如 "user_name = 'lisi1234'"（可选）
        :return: 受影响行数
        """
        try:
            # 如果传了查重条件，先查有没有
            if table and condition:
                self.cursor.execute(f"select * from {table} where {condition}")
                if self.cursor.fetchall():
                    logs.info(f'数据已存在，跳过插入：{table} where {condition}')
                    return 0

            rows = self.cursor.execute(sql)
            self.conn.commit()
            logs.info(f'插入数据库数据成功，受影响行数：{rows}')
            return rows
        except Exception as e:
            logs.error(f'插入数据库数据失败：{e}')
            raise


# if __name__ == '__main__':
#     mysql = ConnectMysql()
#     try:
#         # 删除（不存在就跳过，不报错）
#         mysql.delete('ecs_users', "user_name = 'lisi1234'", must_affect=False)
#
#         # 插入（已存在就跳过）
#         # mysql.insert(
#         #     "insert into ecs_users(user_name, password) values('test001', '123456')",
#         #     table='ecs_users', condition="user_name = 'test001'"
#         # )
#
#         # 更新（不存在就跳过）
#         # mysql.update(
#         #     "update ecs_users set password = 'newpwd' where user_name = 'test001'",
#         #     table='ecs_users', condition="user_name = 'test001'"
#         # )
#
#         # 查询
#         # print(mysql.query("select * from ecs_users limit 1"))
#     finally:
#         mysql.close()