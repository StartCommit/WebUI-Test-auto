import time
import allure
import pytest

from config.setting import is_send_ding
from util_tools.connectMysql import ConnectMysql
from util_tools.dingRebot import send_dd_msg
from util_tools.logs_util.recordlog import logs


@pytest.fixture(scope='session', autouse=True)
@allure.title('进行测试数据清理')
def data_clearing():
    """测试结束后清理测试数据"""
    try:
        conn = ConnectMysql()
    except Exception as e:
        logs.error(f'数据库连接失败，跳过数据清理：{e}')
        yield
        return

    yield
    logs.info('正在清理测试数据')
    try:
        conn.delete('ecs_users', "user_name = 'lisi1234'", must_affect=False)
    except Exception as e:
        logs.error(f'数据清理失败：{e}')
    finally:
        conn.close()


_start_time = None


def pytest_sessionstart(session):
    global _start_time
    _start_time = time.time()


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """pytest预定义的钩子函数，用于自动收集测试结果"""
    total = terminalreporter._numcollected
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    error = len(terminalreporter.stats.get('error', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    duration = round(time.time() - _start_time, 2) if _start_time else 0
    summary = f"""
    自动化测试结束，通知如下，测试结果统计：
    测试用例总数：{total}个
    测试用例通过：{passed}个
    测试用例失败：{failed}个
    测试用例错误：{error}个
    测试用例跳过：{skipped}个
    执行用时：{duration}秒
    """
    if is_send_ding:
        try:
            send_dd_msg(summary)
        except Exception as e:
            logs.error(f'钉钉推送失败：{e}')
