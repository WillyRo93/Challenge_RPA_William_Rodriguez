import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Agregar el directorio del proyecto al path de Python
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)

from news_browser.excel_creator import ExcelCreator

class TestExcelCreator(unittest.TestCase):
    def setUp(self):
        self.creator = ExcelCreator()

    @patch("os.makedirs")
    def test_init_creates_directory(self, mock_makedirs):
        # Arrange
        excel_dir = 'output/excel_files/'

        # Act
        creator = ExcelCreator()

        # Assert
        mock_makedirs.assert_called_once_with(excel_dir, exist_ok=True)

    @patch("os.remove")
    @patch("glob.glob", return_value=["output/excel_files/file1.xlsx", "output/excel_files/file2.xlsx"])
    def test_clear_excel_files(self, mock_glob, mock_remove):
        # Arrange

        # Act
        self.creator.clear_excel_files()

        # Assert
        mock_glob.assert_called_once_with("output/excel_files/*")
        mock_remove.assert_any_call("output/excel_files/file1.xlsx")
        mock_remove.assert_any_call("output/excel_files/file2.xlsx")

    @patch("openpyxl.Workbook.save")
    def test_create_excel(self, mock_save):
        # Arrange
        news_data = [
            {"bool": True, "title": "Title 1", "date": "Date 1", "description": "Description 1", "image_path": "Path 1", "phrase_matches": 1, "contain_money": True},
            {"bool": False, "title": "Title 2", "date": "Date 2", "description": "Description 2", "image_path": "Path 2", "phrase_matches": 2, "contain_money": False},
            {"bool": True, "title": "Title 3", "date": "Date 3", "description": "Description 3", "image_path": "Path 3", "phrase_matches": 3, "contain_money": True}
        ]

        # Act
        self.creator.create_excel(news_data)

        # Assert
        mock_save.assert_called_once_with("output/excel_files/all_news_data.xlsx")

if __name__ == "__main__":
    unittest.main()
