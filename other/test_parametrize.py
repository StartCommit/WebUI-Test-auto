import pytest


class TestParametrize:

    # 参数化一个参数
    @pytest.mark.parametrize("params", ['python', 'java', 'c++'])  # 参数化，列表
    def test_parametrize_01(self, params):  # 参数一定要对应
        print(params)

    # 参数化多个参数，使用列表迭代对象进行参数化
    @pytest.mark.parametrize("username, password", [('admin1', 'admin1'), ('admin', 'admin')])  # 参数化，列表嵌套元组
    def test_login_case(self, username, password):
        print(f'登录,用户名{username} 密码{password}')

    # 使用集合可迭代对象进行参数化
    @pytest.mark.parametrize("username", {('admin1', 'admin1'), ('admin', 'admin'), ('admin2', 'admin2')})  # 参数化，集合
    def test_parametrize_02(self, username):
        print(f'登录,用户名{username}')

    # 使用字典可迭代对象进行参数化
    @pytest.mark.parametrize("user_name", {"admin1": "admin11", "admin2": "admin22"})  # 参数化，字典
    def test_parametrize_03(self, user_name):
        print(f'登录,用户名{user_name}')
