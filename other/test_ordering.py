import pytest


class TestOrdering:

    # @pytest.mark.run(order=3)
    @pytest.mark.last
    def test_ordering_case_01(self):
        print('第一个测试用例')

    # @pytest.mark.run(order=1)
    @pytest.mark.first
    def test_ordering_case_02(self):
        print('第二个测试用例')

    # @pytest.mark.run(order=2)
    @pytest.mark.second
    def test_ordering_case_03(self):
        print('第三个测试用例')


if __name__ == '__main__':
    pytest.main()
