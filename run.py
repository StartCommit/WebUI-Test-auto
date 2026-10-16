import pytest
import os
import shutil
if __name__ == '__main__':
    pytest.main()
    shutil.copy('environment.xml', './report/allure_report')
    os.system('allure serve ./report/allure_report')
