from news_browser.browser import NewsBrowser
from news_browser.my_logger import logger

from robocorp.tasks import task

@task
def main():
    logger.info("*" * 40)
    logger.info("Starting the NewsBrowser Class")
    news_browser = NewsBrowser()

    logger.info("Running the entire process")
    news_browser.run()
    logger.info("*" * 40)

if __name__ == "__main__":
    main()
