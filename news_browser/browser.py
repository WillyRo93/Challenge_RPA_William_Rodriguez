# Standard Python library imports
import json
import os
import time
from datetime import datetime

# Third party libraries imports
from dateutil.relativedelta import relativedelta
from RPA.Browser.Selenium import Selenium
from RPA.Robocorp.WorkItems import WorkItems

# Local module imports
from .excel_creator import ExcelCreator
from .image_downloader import ImageDownloader
from .my_logger import logger
from .news_scraper import NewsScraper
from .utils import (
                    format_current_date,
                    convert_date_to_mm_aaaa,
                    word_counter,
                    does_it_contain_money,
                    calculate_months_to_consider)


class NewsBrowser:
    """
    A class to manage the web browser for scraping news.

    Methods
    -------
    open_news_site(url)
        Opens the news site from a URL
    run()
        Initializes the web browser and runs the news scraper.
    """

    def __init__(self):
        """
        Initializes the NewsBrowser with a headless Chrome WebDriver and configuration settings.
        """
        self.browser = Selenium()
        self.workitems = WorkItems()
        self.workitems.get_input_work_item()  # Load the input work item
        self.news_scraper = NewsScraper(self.browser, self.workitems)
        logger.info(f"Website Configurations Loaded")

    def open_news_site(self, url):
        """
        Opens the news site with the specified URL and search phrase.

        Parameters
        ----------
        url : str
            The URL of the news site.

        Returns
        -------
        None
        """
        logger.info("Starting 'open_news_site' function")
        self.browser.open_available_browser(url, headless=False,
                                            options={"--disable-gpu", "--disable-software-rasterizer"})
        logger.info(f"Opening Website")
        time.sleep(10)

    def run(self):
        """
        Initializes the web browser, runs the news scraper, downloads images, and creates an Excel file.

        Returns
        -------
        None
        """
        logger.info("Starting 'run' function")

        # Obtaining WorkItem Data
        variables = self.workitems.get_work_item_variables()
        search_phrase = variables.get("search_phrase")
        news_category = variables.get("news_category")
        num_months = variables.get("num_months")

        # if os.name == "nt":
        #     search_phrase = "Baseball"
        #     news_category = "Politics"
        #     num_months = 10
        # else:
        #     variables = self.workitems.get_work_item_variables()
        #     search_phrase = variables.get("search_phrase")
        #     news_category = variables.get("news_category")
        #     num_months = variables.get("num_months")

        news_url = "https://www.latimes.com/"
        self.open_news_site(news_url)
        
        # We will have a maximum of 3 retries, in my experience when scraping, more than 5 retries
        # is a bit too much, because something must be wrong in the code or in the site
        # After the maximum tries it could be nice to send an email or any way of notification
        max_retries = 5
        retries = 0
        success = False

        # Here is where we try to open the site and make all the process
        while retries < max_retries and not success:
            try:
                news_data = self.news_scraper.scrap_news(search_phrase, news_category, num_months)
                success = True  # If no exception, mark success as True
            except Exception as e:  # Catch all exceptions for simplicity, you may want to handle specific ones
                retries += 1
                logger.warning(f"An exception occurred: {e}. Retry {retries}/{max_retries}")
                if retries == max_retries:
                    logger.error("Max retries reached. Exiting.")
                    self.browser.close_all_browsers()
                    return  # Exit if max retries reached

        # Finally we quit the open browsers
        self.browser.close_all_browsers()

        # If we succeded opening the site and scraping all the data needed
        # Then based on the news_data list of diccionaries we:
        #   - Download the Necessary Images
        #   - Create the Necessary Excels
        if success and news_data:
            image_downloader = ImageDownloader()
            image_downloader.download_images(news_data)
            time.sleep(1)

            excel_creator = ExcelCreator()
            excel_creator.create_excel(news_data)
            time.sleep(1)
