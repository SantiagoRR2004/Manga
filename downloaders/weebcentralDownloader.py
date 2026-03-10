from .baseDownloader import BaseDownloader
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from modules import Internet
import difflib
import time


class WeebCentralDownloader(BaseDownloader):

    ORIGIN = "https://weebcentral.com/"

    def findChapters(self) -> None:
        """
        This requires to use Selenium without headless mode, because
        Cloudflare blocks otherwise.

        Args:
            - None

        Returns:
            - None
        """
        # Initial empty list
        self.chapterLinks = []

        self.driver = Internet.configureChrome()
        self.driver.minimize_window()

        # Search for the manga
        url = urljoin(self.ORIGIN, "/search?text=" + self.manga.replace(" ", "+"))

        self.driver.get(url)
        time.sleep(5)

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        section = soup.find("section", id="search-results")

        mangas = {}

        # Loop through articles
        for article in section.find_all("article", class_="bg-base-300"):

            link = article.find("a", class_="line-clamp-1")
            if link:
                name = link.get_text(strip=True)
                url = link["href"]
                mangas[name] = url

        if mangas:
            self.foundName = max(
                mangas,
                key=lambda k: difflib.SequenceMatcher(None, k, self.manga).ratio(),
            )
            self.mainUrl = mangas[self.foundName]

            # Go to the manga page
            self.driver.get(self.mainUrl)

            # Click "Show All Chapters" button
            Internet.clickButton(self.driver, "Show All Chapters")
            time.sleep(2)

            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            # Div with id="chapter-list"
            chapterList = soup.find("div", id="chapter-list")

            # Loop through div class="flex items-center"
            for div in chapterList.find_all("div", class_="flex items-center"):
                link = div.find("a", href=True)
                if link:
                    self.chapterLinks.append(link["href"])

            # Fix the order of the chapters
            self.chapterLinks.reverse()

        else:
            self.driver.quit()

    def getChapterImages(self, chapterUrl: str) -> list[str]:
        """
        Get the images of a chapter.

        Args:
            - chapterUrl (str): The url of the chapter

        Returns:
            - list[str]: The list of images
        """
        # Use Selenium
        self.driver.get(chapterUrl)
        time.sleep(2)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        # The section with the images
        section = soup.find("section", {"hx-get": f"{chapterUrl}/images"})

        images = []

        # Iterate through <img>
        for img in section.find_all("img", src=True):
            images.append(img["src"])

        return images
