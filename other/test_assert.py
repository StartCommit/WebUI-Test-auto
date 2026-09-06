import pytest


class TestAssert:
    # 相等断言
    def test_assert_01(self):
        assert 1 + 1 == 2

    # 不相等断言
    def test_assert_02(self):
        assert 1 + 1 == 3

    # 真假断言
    def test_assert_03(self):
        assert_bool = False
        assert assert_bool is True

    # 容器(成员关系)断言
    def test_assert_04(self):
        container = ['python', ' java', ' c++']
        item = 'python'
        assert item in container

    # 集合断言
    def test_assert_05(self):
        set_a = {1, 2, 3}
        set_b = {3, 2, 1}
        assert set_a == set_b


if __name__ == '__main__':
    pytest.main()
