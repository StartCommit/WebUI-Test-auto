import pytest


class TestAddUser:

    @pytest.mark.P1
    def test_add_user_01(self):
        print('新增用户01')

    def test_add_user_02(self):
        print('新增用户02')
    @pytest.mark.P2
    def test_add_user_03(self):
        print('新增用户03')

# 分组执行命令: pytest - vs -m "P1" ，多组命令：pytest -vs -m "P1 or P2"，注意P1,P2要现在pytest.ini中注册