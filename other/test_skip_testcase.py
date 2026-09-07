import pytest


class TestSkipTestCase:

    def test_skip_01(self):
        print('跳过用例01')

    sum = 5

    @pytest.mark.skipif(condition=sum >= 5, reason='大于等于5跳过')  # 条件跳过,condition为True时跳过,reason为跳过原因
    def test_skip_02(self):
        print('跳过用例02')

    @pytest.mark.skip  # 无条件跳过
    def test_skip_03(self):
        print('跳过用例03')

    def test_skip_04(self):
        print('跳过用例04')

    @pytest.mark.xfail # 失败用例
    def test_xfail_case_05(self):
        a= 1
        b = 2
        assert a == b
