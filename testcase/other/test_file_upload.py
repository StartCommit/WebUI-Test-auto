from pageObject.other.file_upload_page import FileUploadPage
import allure


@allure.feature("文件上传模块")
class TestFileUpload:
    @allure.story('文件上传成功')
    @allure.title('选择文件上传成功')
    def test_file_upload_success(self, not_login_driver):
        file = FileUploadPage(not_login_driver)
        file.file_upload()
        # 断言结果
        assert file.get_tag_text(file.assert_result) != ''

    @allure.story('文件上传失败')
    @allure.title('不选文件直接上传')
    def test_file_upload_failed(self, not_login_driver):
        file = FileUploadPage(not_login_driver)
        # 打开页面但不选文件，直接点上传
        file.file_no_upload()
        # 断言：页面上没有出现文件名/大小
        assert file.get_tag_text(file.assert_result) == ''