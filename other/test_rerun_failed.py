import pytest


class TestReRunFailed:

    @pytest.mark.flaky(reruns=3, reruns_delay=2) # 对单个测试用例设置失败重跑的次数和间隔时间
    def test_rerun_fail_case(self):
        import random
        assert random.choice([True, False])

    def test_rerun_fail_case02(self):
        import random
        assert random.choice([True, False])

if __name__ == '__main__':
    pytest.main() #可以写 -v 显示详细日志, -s 显示打印日志, --html=report.html 测试报告, --self-contained-html 测试报告 , --alluredir=allure-results 测试报告， -rerun nun 重跑失败用例
