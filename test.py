# Standard Python library imports
import unittest

# Third party libraries imports
from robocorp.tasks import task

# Local module imports
from news_browser.my_logger import logger
from testing.test_browser import TestNewsBrowser
from testing.test_excel_creator import TestExcelCreator
from testing.test_image_downloader import TestImageDownloader
# from testing.test_news_scraper import TestNewsScraper
from testing.test_utils import TestUtils


@task
def main():
    # Create a TestLoader object to load all unit tests
    loader = unittest.TestLoader()

    # Add the unit tests of each module to the TestSuite
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestExcelCreator))
    suite.addTests(loader.loadTestsFromTestCase(TestImageDownloader))
    suite.addTests(loader.loadTestsFromTestCase(TestNewsBrowser))
    # suite.addTests(loader.loadTestsFromTestCase(TestNewsScraper))
    suite.addTests(loader.loadTestsFromTestCase(TestUtils))


    # Create a TextTestRunner object to run the tests and display the results
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    # Returns True if all tests passed successfully, otherwise False
    return result.wasSuccessful()

if __name__ == "__main__":
    main()