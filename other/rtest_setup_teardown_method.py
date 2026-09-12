class TestSetupTeardownMethod:

    """
    测试用例的前置和后置操作setup_method和teardown_method，测试类中的测试用例执行之前各执行一次前后置操作
    """
    def setup_method(self):
        print('执行测试用例前执行前置操作')

    def test_case_01(self):
        print('第一个测试用例')

    def test_case_02(self):
        print('第二个测试用例')

    def test_case_03(self):
        print('第三个测试用例')

    def teardown_method(self):
        print('执行测试用例后执行后置操作')
