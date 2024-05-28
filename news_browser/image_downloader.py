# Standard Python library imports
import glob
import os

# Third party libraries imports
import requests

# Local module imports
from .my_logger import logger

class ImageDownloader:
    """
    A class to download images from URLs.

    Methods
    -------
    clear_images()
        Clears all existing images in the directory.
    download_images(data)
        Downloads images from the provided data.
    """
    def __init__(self):
        """
        Initializes the ImageDownloader, sets the directory for images,
        and clears existing images.
        """
        # Here we provide a directory to the code, this directory will or may have some previous documents
        # Those documents are not of our interest right now, so we delete them
        # The function "clear_images()" stablish how we delete the files
        self.imgs_dir = 'output/'
        os.makedirs(self.imgs_dir, exist_ok=True)
        self.clear_images()

    def clear_images(self):
        """
        Clears all existing images in the directory.

        Returns
        -------
        None
        """
        logger.info("Starting 'clear_images' function")

        # Here is how we delete all the files
        files = glob.glob(f"{self.imgs_dir}*.jpg")
        for f in files:
            os.remove(f)
        logger.info("All Image Files Cleared")

    def download_images(self, news_data):
        """
        Downloads images from the provided data and saves them to the directory.

        Parameters
        ----------
        news_data : list of dict
            List of dictionaries containing the image URLs and other related information.

        Returns
        -------
        None
        """
        logger.info("Starting 'download_images' function")

        logger.info("Creating the necessary Excel Files")
        # Once we have the "news_data" list of dictionaries, we iterate over it
        for item in news_data:
            # Here we obtain the "bool" value of our current dictionay as well as its url
            image_url = item.get("image_url")
            news_boolean = item.get("bool")
            # If the key "bool" is True, then we proceed, also if the url is not "N/A"
            # What this Boolean value means is that the new that it contains is or is not of our interest.
            #   - {"bool": True} Means that we will create an Excel for this news
            #   - {"bool": False} Means that we will NOT create an Excel for this news
            # And the URL may be "N/A" because the site news did not post any pic for it
            if image_url and image_url != "N/A" and news_boolean:
                response = requests.get(image_url)
                if response.status_code == 200:
                    image_path = os.path.join(self.imgs_dir, f"{item['news_name']}.jpg")
                    with open(image_path, "wb") as f:
                        f.write(response.content)
                    item["image_path"] = image_path
                else:
                    logger.error(f"Failed to download image from {image_url}")


        logger.info(f"All necessary Image Files created")
