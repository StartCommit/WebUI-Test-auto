import pytest


class TestLogin01:
    def test_case_01(self):
        print('pytest主函数模式')
        assert 1 + 1 == 2

    def test_case_02(self):
        print('pytest命令行模式')
        assert 1 + 3 == 4


class TestLogin02:
    def test_case_01(self):
        print('pytest主函数模式1')
        assert 1 + 1 == 2

    def test_case_02(self):
        print('pytest命令行模式2')
        assert 1 + 3 == 4

    def test_case_03(self):
        print('pytest命令行模式3')
        assert 1 + 2 == 3


if __name__ == '__main__':
    pytest.main()  # -v 显示详细日志, -s 显示打印日志
