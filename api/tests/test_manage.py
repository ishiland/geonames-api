from tests.base import BaseTestCase
import os
from manage import download_and_extract, data_path


# TODO: mock the requests for this test
class TestManageCommands(BaseTestCase):
    """Tests commands from manage.py"""
    pass
    # def test_download_and_extract_zip(self):
    #     """tests downloading of text file"""
    #     file = 'readme.txt'  # 8.5kb
    #     output = download_and_extract(file)
    #     self.assertEqual(output, os.path.join(data_path, file))
    #
    # def test_download_and_extract_no_zip(self):
    #     """tests downloading and extracting of zip file"""
    #     file = 'YU.zip'  # 3.7kb
    #     output = download_and_extract(file)
    #     self.assertEqual(output, os.path.join(data_path, 'YU.txt'))
