import pytest


# 1）pytest.fixture不带参数
@pytest.fixture
def init_browser(request):
    print("前置操作，初始化浏览器对象")

    def teardown():
        print("后置操作，关闭浏览器对象，清理数据")

    request.addfinalizer(teardown)  # 将teardowen函数注册为最终器，以确保在测试用例运行结束后执行后置操作
    return teardown


# 2）pytest.fixture yield关键字
@pytest.fixture
def init_browser2():
    print("前置操作，初始化浏览器对象")

    yield  # yield 后面的代码将作为测试用例的返回值
    print("后置操作，关闭浏览器对象，清理数据")


# 3)pytest.fixture参数
"""
@pytest.fixture(scope='function',autouse=True,params='', ids='',name='')
scope:控制fixture的作用域，可选值 function, class, module, session
    function: 每个测试函数执行前后各执行一次,
    class: 每个测试类执行前后执行一次, 
    module: 每个测试模块执行一次（每个.py文件）执行一次, 
    session: 整个pytest会话（多个模块）执行前后执行一次
autouse:是否自动执行，默认为False,为True时，fixture会自动执行，不需要手动调用，即不需要写函数调用
ids:为参数化的fixture提供自定义的标识，用于在测试报告中更清晰的显示参数
name:为fixture提供自定义的名称
"""


@pytest.fixture(scope='class', autouse=True)
def init_browser3():
    print("前置操作，初始化浏览器对象")
    yield  # yield 后面的代码将作为测试用例的返回值
    print("后置操作，关闭浏览器对象，清理数据")


"""
params:用于参数化的一个选项，他允许你为fixture定义多个参数，以便在测试函数中使用不同的参数组合进行测试
"""


@pytest.fixture(params=['apple', 'banana', 'orange'], ids=['苹果', '香蕉', '橘子'], name='setup_init')
def setup(request):
    value = request.param
    return value


class TestFixture:
    # 如果前置函数@pytest.fixture不带参数，需要手动使用前置

    def test_case_01(self, init_browser):
        print('fixture的第一个测试用例')

    def test_case_02(self, init_browser):
        print('fixture的第二个测试用例')

    def test_case_03(self, init_browser2):
        print('fixture1的第一个测试用例')

    def test_case_04(self, init_browser2):
        print('fixture1的第二个测试用例')

    def test_case_05(self, init_browser3):
        print('fixture1的第一个测试用例')

    def test_case_06(self, init_browser3):
        print('fixture1的第二个测试用例')

    def test_case_07(self):
        print('fixture1的第一个测试用例')

    def test_case_08(self):
        print('fixture1的第二个测试用例')

    def test_case_09(self, setup_init):
        assert len(setup_init) > 0
