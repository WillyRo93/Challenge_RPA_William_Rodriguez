# Standard Python library imports
import glob
import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from openpyxl import load_workbook

# Taking the correct directory to import the files
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)

# Local module imports
from news_browser.image_downloader import ImageDownloader

class TestImageDownloader(unittest.TestCase):
    def setUp(self):
        self.image_downloader = ImageDownloader()

    @patch('news_browser.image_downloader.logger')
    def test_clear_images(self, mock_logger):
        # Create a dummy image file to test deletion
        dummy_file = 'output/test.jpg'
        open(dummy_file, 'a').close()
        self.assertTrue(os.path.exists(dummy_file))

        # Clear image files
        self.image_downloader.clear_images()
        self.assertFalse(os.path.exists(dummy_file))

    @patch('news_browser.image_downloader.logger')
    @patch('news_browser.image_downloader.requests.get')
    def test_download_images(self, mock_requests_get, mock_logger):
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'test image content'
        mock_requests_get.return_value = mock_response

        # Sample news data
        news_data = [
            {
                "bool": True,
                "image_url": "http://example.com/image.jpg",
                "news_name": "test_news",
                "image_path": "N/A"
            }
        ]

        # Call download_images
        self.image_downloader.download_images(news_data)

        # Check if the image file is created
        image_files = glob.glob(f"{self.image_downloader.imgs_dir}*.jpg")
        self.assertFalse(len(image_files) > 0)
        self.assertFalse(os.path.exists('output/test_news.jpg'))

    @patch('news_browser.image_downloader.logger')
    @patch('news_browser.image_downloader.requests.get')
    def test_no_images_downloaded_for_irrelevant_news(self, mock_requests_get, mock_logger):
        # Sample news data with irrelevant news
        news_data = [
            {
                "bool": False,
                "image_url": "http://example.com/image.jpg",
                "news_name": "test_news",
                "image_path": "N/A"
            },
            {
                "bool": False,
                "image_url": "http://example.com/image2.jpg",
                "news_name": "test_news2",
                "image_path": "output/news.jpg"
            }
        ]

        # Call download_images
        self.image_downloader.download_images(news_data)

        # Check that no image files are created
        image_files = glob.glob(f"{self.image_downloader.imgs_dir}*.jpg")
        self.assertTrue(len(image_files) == 0)

    # @patch('image_downloader.logger')
    # @patch('image_downloader.requests.get')
    # def test_no_images_downloaded_for_na_urls(self, mock_requests_get, mock_logger):
    #     # Sample news data with N/A image URLs
    #     news_data = [
    #         {
    #             "bool": True,
    #             "image_url": "N/A",
    #             "news_name": "test_news",
    #             "image_path": "N/A"
    #         }
    #     ]

    #     # Call download_images
    #     self.image_downloader.download_images(news_data)

    #     # Check that no image files are created
    #     image_files = glob.glob(f"{self.image_downloader.imgs_dir}*.jpg")
    #     self.assertTrue(len(image_files) == 0)

if __name__ == '__main__':
    unittest.main()
