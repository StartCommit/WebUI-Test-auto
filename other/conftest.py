import pytest
from util_tools.logs_util.recordlog import logs

"""
conftest.py文件是一个单独存放的测试夹具，pytest会自动搜索conftest.py文件并执行其中的测试夹具。
可以创建多个conftest.py文件，每个conftest.py文件会对其所在目录及其子目录下的测试模块生效。
在不同模块的测试中需要用到conftest.py的前后置功能时，不需要做任何的import导入操作
作用:可以在不同的py文件中使用同一个fixture函数
"""


@pytest.fixture(scope='function', autouse=True)
def info_output():
    logs.info('——————测试用例开始执行——————')
    yield
    logs.info('——————测试用例结束执行——————')
