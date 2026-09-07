import pytest


class TestDeleteUser:

    @pytest.mark.P1
    def test_delete_user_01(self):
        print("删除用户01")

    def test_delete_user_02(self):
        print("删除用户02")
    @pytest.mark.P2
    def test_delete_user_03(self):
        print('删除用户03')
