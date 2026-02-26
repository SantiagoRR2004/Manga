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

        Need to use Selenium to find the manga, then the reading list
        and finally the chapter list.

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

        options = {}

        for div in mangaDiv.find_all("div", class_="manga-card"):
            aTag = div.find("a", class_="font-bold title", href=True)

            if aTag:
                name = aTag.text.strip()
                options[name] = urljoin(self.ORIGIN, aTag["href"].strip())

        if options:
            # Find the best match
            self.foundName = max(
                options,
                key=lambda k: difflib.SequenceMatcher(None, k, self.manga).ratio(),
            )
            self.mainUrl = options[self.foundName]

            # Need to find the reading list
            driver.get(self.mainUrl)
            time.sleep(2)

            soup2 = BeautifulSoup(driver.page_source, "html.parser")

            # Div with class "chapter relative read"
            firstDiv = soup2.find("div", class_="chapter relative read")
            # Found the reading list
            self.mainUrl = urljoin(
                self.ORIGIN, firstDiv.find("a", href=True)["href"].strip()
            )

            # Now we get the chapter list
            driver.get(self.mainUrl)
            time.sleep(2)
            soup3 = BeautifulSoup(driver.page_source, "html.parser")

            # Iterate across li with data-value attribute
            for li in soup3.find("div", class_="mr-2 ml-2 flex-grow").find_all(
                "li", attrs={"data-value": True}
            ):
                url = urljoin(self.ORIGIN, "chapter/" + li["data-value"].strip())
                self.chapterLinks.append(url)

            # Reverse the chapter links to have them in order
            self.chapterLinks.reverse()

        if len(self.chapterLinks) == 0:
            driver.quit()

    def getChapterImages(self, chapterUrl: str) -> list[str]:
        # TODO
        return []
