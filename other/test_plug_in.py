import pytest
from time import sleep


class TestPugIn:

    def test_plug_case_01(self):
        sleep(3)
        print('pytest主函数模式')

    def test_plug_case_02(self):
        sleep(3)
        print('pytest命令行模式')

    def test_plug_case_03(self):
        sleep(3)
        print('pytest命令行模式3')


if __name__ == '__main__':
    pytest.main(['-n=3'])
