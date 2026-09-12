class TestSetupTeardownClass:

    """
    测试用例的前置和后置操作setup_class 和 teardown_class，测试类中的测试用例执行前只执行一次
    """
    def setup_class(self):
        print('执行测试用例前执行前置操作')

    def test_case_01(self):
        print('第一个测试用例')

    def test_case_02(self):
        print('第二个测试用例')

    def test_case_03(self):
        print('第三个测试用例')

    def teardown_class(self):
        print('执行测试用例后执行后置操作')
