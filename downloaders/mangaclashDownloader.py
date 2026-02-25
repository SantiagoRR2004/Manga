from .baseDownloader import BaseDownloader
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from modules import Internet
import difflib
import time


class MangaClashDownloader(BaseDownloader):

    ORIGIN = "https://toonclash.com/"

    def findChapters(self) -> None:
        """
        Finds the chapters of the manga and stores them in the chapterLinks attribute.

        Need to use Selenium and there is a big probability
        that Cloudflare blocks the connection.

        Args:
            - None

        Returns:
            - None
        """
        # Initial empty list
        self.chapterLinks = []

        self.driver = Internet.configureChrome()

        # Use query parameters to search for the manga
        url = urljoin(
            self.ORIGIN, "/?s=" + self.manga.replace(" ", "+") + "&post_type=wp-manga"
        )

        # Pretend to arrive and then search
        self.driver.get(self.ORIGIN)
        time.sleep(5)
        self.driver.get(url)
        time.sleep(5)

        # Obtain the html
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        options = {}
        # Iterate across divs with class "row c-tabs-item__content"
        for div in soup.find_all("div", class_="row c-tabs-item__content"):

            aTag = div.find("a", title=True, href=True)

            if aTag:
                name = aTag["title"].strip()
                url = aTag["href"].strip()
                options[name] = url

        if options:
            # Find the best match
            self.foundName = max(
                options,
                key=lambda k: difflib.SequenceMatcher(None, k, self.manga).ratio(),
            )
            self.mainUrl = options[self.foundName]

            self.driver.get(self.mainUrl)
            time.sleep(1)
            soup2 = BeautifulSoup(self.driver.page_source, "html.parser")

            # Find div with class "page-content-listing single-page"
            div = soup2.find("div", class_="page-content-listing single-page")
            for aTag in div.find_all("a", href=True):
                url = aTag["href"].strip()
                self.chapterLinks.append(url)

            # Reverse the list to have the chapters in order
            self.chapterLinks.reverse()

    def getChapterImages(self, chapterUrl: str) -> list[str]:
        """
        Returns the list of image urls for a given chapter url.

        We need to use Selenium and scroll until the bottom
        is reached to load all the images.

        Args:
            - chapterUrl (str): The url of the chapter to get the images from.

        Returns:
            - list[str]: The list of image urls for the chapter.
        """
        self.driver.get(chapterUrl)

        lastHeight = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(2)

            newHeight = self.driver.execute_script("return document.body.scrollHeight")
            if newHeight == lastHeight:
                break
            lastHeight = newHeight

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        images = []

        # Iterate across divs with class "page-break no-gaps"
        for div in soup.find_all("div", class_="page-break no-gaps"):
            img = div.find("img", src=True)
            if img:
                images.append(img["src"])

        return images
