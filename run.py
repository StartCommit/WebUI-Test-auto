# import pytest
# import os
# import shutil
# if __name__ == '__main__':
#     pytest.main()
#     shutil.copy('environment.xml', './report/allure_report')
#     os.system('allure serve ./report/allure_report')
import pytest
import os
import shutil
from pathlib import Path


def inject_chinese_js(report_dir):
    """向静态报告注入中文配置"""
    index_path = Path(report_dir) / 'index.html'
    if not index_path.exists():
        print(f"⚠️ 找不到 {index_path}，生成报告可能失败。")
        return

    html_content = index_path.read_text(encoding='utf-8')

    js_code = """
    <script>
        let settings = JSON.parse(localStorage.getItem('ALLURE_REPORT_SETTINGS')) || {};
        settings.language = "zh";
        localStorage.setItem('ALLURE_REPORT_SETTINGS', JSON.stringify(settings));
    </script>
    """

    if "settings.language = \"zh-CN\";" not in html_content:
        html_content = html_content.replace('</head>', f'{js_code}\n</head>')
        index_path.write_text(html_content, encoding='utf-8')
        print("✅ 中文配置已成功注入静态报告！")


def clean_old_reports(*dirs):
    """清理旧的测试结果和报告目录"""
    for d in dirs:
        if os.path.exists(d):
            try:
                shutil.rmtree(d)
                print(f"🧹 已清理旧目录：{d}")
            except Exception as e:
                print(f"⚠️ 清理目录 {d} 失败：{e}")


if __name__ == '__main__':
    # 1. 定义路径
    data_dir = './report/allure_report'  # 原始数据存放目录
    static_report_dir = './report/html'  # 最终静态 HTML 存放目录

    # 2. ⚠️ 核心：每次执行前，先把旧的报告和数据全删掉！
    clean_old_reports(data_dir, static_report_dir)

    # 3. 运行测试
    pytest.main()

    # 4. 复制环境信息到数据目录
    if os.path.exists('environment.xml'):
        # 因为刚清理过，所以需要先确保目录存在
        os.makedirs(data_dir, exist_ok=True)
        shutil.copy('environment.xml', data_dir)
        print("✅ environment.xml 已复制到数据目录")

    # 5. 生成静态 HTML 报告（虽然加了 --clean，但上面已经彻底清理过一遍了，双重保险）
    print("正在生成静态 HTML 报告...")
    os.system(f'allure generate {data_dir} -o {static_report_dir} --clean')

    # 6. 注入中文化脚本
    inject_chinese_js(static_report_dir)

    # 7. 自动打开预览
    print("正在打开报告...")
    os.system(f'allure open {static_report_dir}')