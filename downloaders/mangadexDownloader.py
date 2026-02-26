from .baseDownloader import BaseDownloader
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from modules import Internet
import difflib
import time


class MangaDexDownloader(BaseDownloader):

    ORIGIN = "https://mangadex.org/"

    def findChapters(self) -> None:
        """
        Find the chapters of the manga and store them in the chapterLinks attribute.

        Need to use Selenium to find the manga.

        Args:
            - None

        Returns:
            - None
        """
        # Initial empty list
        self.chapterLinks = []

        driver = Internet.configureChrome()

        url = urljoin(
            self.ORIGIN, "/search?q=" + self.manga.replace(" ", "+") + "&tab=titles"
        )
        driver.get(url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # First find the div with class "md-content flex-grow"
        # Find a div without class inside it
        mangaDiv = [
            div
            for div in soup.find("div", class_="md-content flex-grow").find_all("div")
            if not div.get("class")
        ][0]

        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(str(mangaDiv))

        options = {}

        for div in mangaDiv.find_all("div", class_="manga-card"):
            aTag = div.find("a", class_="font-bold title", href=True)

            if aTag:
                name = aTag.text.strip()
                url = urljoin(self.ORIGIN, aTag["href"].strip())
                options[name] = url

        if options:
            # Find the best match
            self.foundName = max(
                options,
                key=lambda k: difflib.SequenceMatcher(None, k, self.manga).ratio(),
            )
            self.mainUrl = options[self.foundName]

            print(self.mainUrl)

    def getChapterImages(self, chapterUrl: str) -> list[str]:
        # TODO
        return []
