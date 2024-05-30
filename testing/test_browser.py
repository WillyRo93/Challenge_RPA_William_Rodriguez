# Standard Python library imports
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Taking the correct directory to import the files
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)

# Local module imports
from news_browser.browser import NewsBrowser

class TestNewsBrowser(unittest.TestCase):
    
    @patch("news_browser.browser.Selenium")
    @patch("news_browser.browser.WorkItems")
    @patch("news_browser.browser.NewsScraper")
    def setUp(self, MockNewsScraper, MockWorkItems, MockSelenium):
        # Mock the dependencies
        self.mock_browser = MockSelenium.return_value
        self.mock_workitems = MockWorkItems.return_value
        self.mock_news_scraper = MockNewsScraper.return_value
        
        # Create instance of NewsBrowser
        self.news_browser = NewsBrowser()
        
        # Set up the mock return values for work items
        self.mock_workitems.get_work_item_variables.return_value = {
            "search_phrase": "Trump",
            "news_category": "World & Nation",
            "num_months": 1
        }

    def test_open_news_site(self):
        # Arrange
        url = "https://www.latimes.com/"
        
        # Act
        self.news_browser.open_news_site(url)
        
        # Assert
        self.mock_browser.open_available_browser.assert_called_once_with(
            url, headless=False, options={"--disable-gpu", "--disable-software-rasterizer"}
        )
        self.assertTrue(self.mock_browser.open_available_browser.called)
    
    @patch("news_browser.browser.validate_input", return_value=True)
    @patch("news_browser.browser.ExcelCreator")
    @patch("news_browser.browser.ImageDownloader")
    @patch("time.sleep", return_value=None)  # To speed up the test execution
    def test_run(self, mock_sleep, MockImageDownloader, MockExcelCreator, mock_validate_input):
        # Arrange
        mock_image_downloader = MockImageDownloader.return_value
        mock_excel_creator = MockExcelCreator.return_value
        self.mock_news_scraper.scrap_news.return_value = [
            {"bool": True, "title": "Title 1", "date": "Date 1", "description": "Description 1", "image_url": "http://example.com/image1.jpg", "phrase_matches": 1, "contain_money": True}
        ]
        
        # Act
        self.news_browser.run()
        
        # Assert
        self.mock_browser.open_available_browser.assert_called()
        self.mock_news_scraper.scrap_news.assert_called_with("Trump", "World & Nation", 1)
        mock_image_downloader.download_images.assert_called()
        mock_excel_creator.create_excel.assert_called()
        self.mock_browser.close_all_browsers.assert_called()

    @patch("news_browser.browser.validate_input", return_value=False)
    def test_run_invalid_input(self, mock_validate_input):
        # Act
        self.news_browser.run()
        
        # Assert
        self.mock_browser.open_available_browser.assert_not_called()
        self.mock_news_scraper.scrap_news.assert_not_called()

if __name__ == '__main__':
    unittest.main()
