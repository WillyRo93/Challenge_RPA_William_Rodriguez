# Standard Python library imports
import time

# Third party libraries imports
from bs4 import BeautifulSoup
from RPA.Browser.Selenium import Selenium
# from RPA.Browser.Selenium import exec_javascript
# from RPA.Excel.Files import ExcelFile
from RPA.Robocorp.WorkItems import WorkItems

# Local module imports
from .my_logger import logger
from .utils import (
    format_current_date,
    convert_date_to_mm_aaaa,
    word_counter,
    does_it_contain_money,
    calculate_months_to_consider
)


class NewsScraper:
    """
    A class to scrape news articles from a website using Selenium.

    Parameters
    ----------
    browser : RPA.Browser.Selenium.Browser
        The Selenium Browser instance used to interact with the website.
    config : dict
        Configuration dictionary containing search parameters and other settings.

    Methods
    -------
    no_results_search()
        Checks if the search query returned no results.
    search_news()
        Performs a search on the website based on the provided configuration.
    scrap_news()
        Scrapes the news articles from the search results.
    """

    def __init__(self, browser, workitems):
        """
        Initializes the NewsScraper with a WebDriver and configuration.

        Parameters
        ----------
        browser : RPA.Browser.Selenium.Browser
            The Selenium Browser instance used to interact with the website.
        config : dict
            Configuration dictionary containing search parameters and other settings.
        """
        self.browser = browser
        self.workitems = workitems

    def no_results_search(self):
        """
        Checks if the search query returned no results.

        Returns
        -------
        bool
            True if no results were found, False otherwise.
        """
        logger.info("Starting 'no_results_search' function")

        # Here we try to obtain the element that contains 'There are not any results that match ...'
        # This is because some searches may find nothing and that needs to be catched
        try:
            no_results_locator = "class:search-results-module-no-results"
            self.browser.wait_until_element_is_visible(no_results_locator, timeout = 20)
            inner_text = self.browser.get_text(no_results_locator)
            logger.info(inner_text)
            time.sleep(1)
            return "There are not any results that match" in inner_text
        except:
            logger.info("There are results that match")
            return False

    def search_news(self, search_phrase, news_category):
        """
        Performs a search on the website based on the provided configuration.

        Returns
        -------
        bool
            True if the search was successful, False otherwise.
        """
        logger.info("Starting 'search_news' function")

        # We try to locate the search button and input
        search_button = 'css:button[data-element="search-button"]'
        self.browser.wait_until_element_is_visible(search_button, timeout=20)
        self.browser.click_element(search_button)
        logger.info("We found the search locator and we clicked on it")
        time.sleep(1)

        search_input = 'css:input[data-element="search-form-input"]'
        self.browser.wait_until_element_is_visible(search_input, timeout=20)
        self.browser.click_element(search_input)
        self.browser.press_keys(search_input, search_phrase + "\n")
        logger.info(f"We found the input locator and we searched '{search_phrase}'")
        time.sleep(2)

        # Here we call the 'no_results_search()' function to see if there were not results
        if self.no_results_search():
            logger.warning(f"No results found for search: {search_phrase}")
            return False

        # We directly select the 'Newest' option from 'Sort By' dropdown button
        newest = "css:select.select-input"
        self.browser.select_from_list_by_label(newest, 'Newest')
        logger.info("We succesfully selected the 'Newest' option")
        time.sleep(1)

        # We locate the Filter Button and click on it
        # If the site opens maximized there is no need to do this but there is
        # not any error clicking on it on that case so we dont overcode here if not needed
        filter_button = "css:button.button.filters-open-button"
        filter_visible = self.browser.is_element_visible(filter_button)
        if filter_visible:
            self.browser.click_element(filter_button)
            logger.info("We succesfully clicked the 'Filters' button")
            time.sleep(1)

        logger.info("There was not a 'Filters' button visible") # This is the case that 'Filters' button is not found

        # The topics are hidden by an element, so we click on 'See All' button to see all topics
        see_all_button = "css:span.see-all-text"
        self.browser.wait_until_element_is_visible(see_all_button, timeout=20)
        self.browser.click_element(see_all_button)
        logger.info("We succesfully clicked the 'See all' button")
        time.sleep(1)

        # Here we obtain all data contained on the 'topic box'.
        # Thats how I called it, a box that contains all topics
        topics_box = "css:ul.search-filter-menu"
        self.browser.wait_until_element_is_visible(topics_box, timeout=20)
        topics_box = self.browser.get_webelement(topics_box)
        logger.info("We succesfully found the box with all the topics")
        logger.debug(f"topics_box = {topics_box}")


        # Here, we obtain the topic click-box element for every topic on the website
        # This needs some revision because later we will iterate over it
        # Since I dont dominate RPA.Browser.Selenium, I dont really know how to get some info from web elements
        # As I do from pure Selenium, you will see later on the next cycle why this needs revision
        topic_element = "css:div.search-filter-input.SearchFilterInput div.checkbox-input input.checkbox-input-element"
        # topics_elements = self.browser.get_webelements("css:ul.search-filter-menu > li") ## This is in case we knew how to handle list info correctly
        topics_elements = self.browser.get_webelements(topic_element)
        logger.info("And now from the topic box, we have all topic names")
        logger.info(f"Number of topic found {len(topics_elements)}")
        logger.debug(f"topics_elements = {topics_elements}")

        # Here we declare a 'soup' variable that gets all HTML info from the topic box
        # So we later iterate over it to find the inner text which contains the topic names
        soup = BeautifulSoup(topics_box.get_attribute("outerHTML"), "html.parser")
        topics_list = soup.find_all('li')
        logger.info("And now from the topic box, we have all topic names")
        logger.debug(f"topics_list = {topics_list}")

        # Ok, lets find out what this cycle does
        #   - topics_list: Contains all list (li) values from the topic box
        #   - topics_elements: Contains all box input elements for all the topics
        # Why we iterate with zip? I tried many different ways to obtain the input element from a current element
        # And I tried many things:
        #   - JavaScript Executions
        #   - Beautiful Soup Find by Tag, Class, etc
        # But could not find any wat to find the box element, so I directly found all input elements previously to keep it going
        # Why do I say it needs revision? Because this is not clean, if the elements found are not in the same order as the
        # topic list, then I will click another input box, so I will find news from a different Topic than asked.
        for topic, topic_element in zip(topics_list, topics_elements):
            # logger.debug(f"topic = {topic}")
            all_span = topic.find_all('span')
            for span in all_span:
                topic_text = span.get_text(strip=True)
                logger.debug(f"We compare {topic_text} with {news_category}")
                if topic_text.lower() == news_category.lower():
                    logger.info(f"Found a matching category which is {topic_text}")
                    logger.debug(f"topic = {topic}")
                    logger.debug(f"topic_element = {topic_element}")
                    self.browser.click_element(topic_element)
                    # Just for debug we could take some screenshots of the element(s) we are getting
                    # filename = self.browser.capture_element_screenshot(topic_element, "element_screenshot.png")
                    # logger.info(self.browser.capture_element_screenshot(topic_element, "element_screenshot.png"))

                    time.sleep(2)
                    logger.info("We clicked the topic")

                    # We try to click the apply button, if we cant its mostly because it was not needed
                    # Sometimes the site, when clicking the topic box, starts the search automatically
                    # Some other times, it does not, so we click the apply button if it is visible.
                    try:
                        apply_button = "css:button.button.apply-button"
                        self.browser.click_element(apply_button)
                        logger.info("We succesfully clicked the 'apply' button")
                        time.sleep(3)
                    except Exception as e:
                        logger.warning("Maybe we could not find the 'Apply' button")
                        logger.warning("Or the Search was done previously when clicking the topic")
                        logger.warning(f"Did not find the 'Apply' button: {e}")

                    # Here, we return True because we found a match for the topic
                    #So, there is no reason to keep looking for topic matches.
                    return True
            
            # We declare the variable 'topic_element' as False, because if the procces did not previously returned
            # a True value, then it is because there was not match found for the topic
            topic_element = False

        # If there is not a Topic Element found to click, then the Topic does not exist or we could not find it
        if not topic_element:
            logger.warning(f"No '{news_category}' category found for search '{search_phrase}'")
            return False

        # return True

    def scrap_news(self, search_phrase, news_category, num_months):
        """
        Scrapes the news articles from the search results.

        Returns
        -------
        list of dict
            A list of dictionaries containing the scraped news data.
        """
        logger.info("Starting scrap_news function")

        # Here we call the 'search_news' function
        if not self.search_news(search_phrase, news_category):
            return []

        # There is a subscription limit (I guess) which limits us to only 10 pages
        subscription, max_pages = False, 10

        # We initialize the news_data list which will contain all news info in dictionaries
        news_data = []
        index = 1

        # We call the function to return us what months and years will be considered for the scraping
        months_to_consider = calculate_months_to_consider(num_months)
        logger.info(months_to_consider)

        # For kind of debug, we obtain the number of pages that the search returns
        try:
            number_of_pages = "css:div.search-results-module-page-counts"
            self.browser.wait_until_element_is_visible(number_of_pages, timeout=20)
            number_of_pages = self.browser.get_webelement(number_of_pages)
            number_of_pages = self.browser.get_text(number_of_pages)
            logger.info(f"Number of pages for searching '{search_phrase}' with the topic '{news_category}': {number_of_pages}")
        except Exception as e:
            logger.warning(f"Maybe searching for '{search_phrase} on the topic '{news_category}' found only one page")
            logger.warning(f"Did not find the 'Number of pages' text: {e}")
        #return True

        # We initialize the index in 1 because is easer to debug and find the news in the files later manually
        # (At least it is easier for me)
        for page_number in range(1, max_pages + 1):
            # logger.info(f"Currently on the page number {number_of_pages}")

            # Here we obtain all the news info whic is contained in some kind of box (I say it is kind of a box)
            news_box = "class:search-results-module-results-menu"
            self.browser.wait_until_element_is_visible(news_box, timeout=20)
            news_box = self.browser.get_webelement(news_box)
            logger.info("Succesfully obtained the WebElement that contains the news")
            logger.debug(f"news_box = {news_box}")

            # We declare a 'soup' variable from which we will obtain all the data needed
            soup = BeautifulSoup(news_box.get_attribute("outerHTML"), "html.parser")
            news_items = soup.find_all('div', class_='promo-wrapper')
            logger.info("We obtained as well the 'promo-wrapper' info, which contains everything we need")
            logger.debug(f"news_items = {news_items}")

            # Now we iterate for every item in the list of dictionaries
            # We find for every item:
            #   - Title
            #   - Description
            #   - Date
            #   - Image TAG (Not used for next steps)
            #   - Image URL
            for item in news_items:
                title_tag = item.find('h3', class_='promo-title')
                title = title_tag.text.strip() if title_tag else 'N/A'
                
                desc_tag = item.find('p', class_='promo-description')
                desc = desc_tag.text.strip() if desc_tag else 'N/A'

                text_to_match = title + desc
                match_count = word_counter(text_to_match, search_phrase)
                contain_money = does_it_contain_money(text_to_match)

                time_tag = item.find('p', class_='promo-timestamp')
                my_date = time_tag.text.strip() if time_tag else 'N/A'

                image_tag = item.find('img', class_='image')
                image_url = image_tag.get("src") if image_tag else "N/A"
                image_alt = image_tag.get("alt") if image_tag else "N/A"
                image_path = f"output/news{index}.jpg" if image_tag else "N/A"

                formatted_date = convert_date_to_mm_aaaa(my_date)
                boolean = formatted_date in months_to_consider

                news_data.append({
                    "title": title,
                    "date": my_date,
                    "description": desc, 
                    'image_url': image_url,
                    'image_alt': image_alt,
                    "phrase_matches": match_count,
                    "contain_money": contain_money,
                    "news_name": f"news{index}",
                    "image_path": image_path,
                    "excel_filename": f"output/excel_files/news{index}.xlsx",
                    "bool": boolean 
                })

                index += 1

            logger.info("We succesfully obtained the title, description and url of all the news")
            logger.debug(f"news_data = {news_data}")

            # Then, if every item in my list of dictionaries is True and we have not reached the maximum number of pages
            # We proceed to click the next page element, so we clearly go to the next page.
            if all(item['bool'] for item in news_data) and page_number < max_pages:
                next_page = "class:search-results-module-next-page"
                self.browser.wait_until_element_is_visible(next_page, timeout=20)
                self.browser.click_element(next_page)
                logger.info("Succesfully clicked the 'Next Page' button")
                time.sleep(5)
            else:
                if subscription:
                    logger.warning("Subscription is enabled, but scraping beyond page 10 is not yet implemented.")
                    break
                if not subscription and page_number == max_pages:
                    logger.warning("Reached the maximum number of pages for non-subscription users.")
                    break
                else:
                    break

        logger.debug(f"Collected news data: {news_data}")
        return news_data
