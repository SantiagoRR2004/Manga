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

        self.driver = Internet.configureChrome()

        # Get the possible mangas
        mangas = self.getOptions()

        if mangas:
            # Find the best match
            self.foundName = max(
                mangas,
                key=lambda k: difflib.SequenceMatcher(None, k, self.manga).ratio(),
            )
            self.mainUrl = mangas[self.foundName]

            # Now we get the reading list
            if self.findReadingList():

                # The chapter list
                self.chaptersInsideReadingList()

        if len(self.chapterLinks) == 0:
            self.driver.quit()

    def getOptions(self) -> dict:
        """
        Get the different possible mangas.

        Args:
            - None

        Returns:
            - dict: A dictionary with the options for the manga.
        """
        initialUrl = urljoin(
            self.ORIGIN, "/search?q=" + self.manga.replace(" ", "+") + "&tab=titles"
        )

        self.driver.get(initialUrl)
        time.sleep(2)

        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        # First find the div with class "md-content flex-grow"
        container = soup.find("div", class_="md-content flex-grow")

        if container:
            # Find a div without class inside it
            noClass = [div for div in container.find_all("div") if not div.get("class")]

            if noClass:
                # The first one
                mangaDiv = noClass[0]

                options = {}

                for div in mangaDiv.find_all("div", class_="manga-card"):
                    aTag = div.find("a", class_="font-bold title", href=True)

                    if aTag:
                        name = aTag.text.strip()
                        options[name] = urljoin(self.ORIGIN, aTag["href"].strip())

                return options

        return {}

    def findReadingList(self) -> bool:
        """
        Find the reading list of the manga.

        Args:
            - None

        Returns:
            - bool: True if the reading list was found, False otherwise.
        """
        self.driver.get(self.mainUrl)
        time.sleep(2)

        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        # Div with class "chapter relative read"
        firstDiv = soup.find("div", class_="chapter relative read")

        if firstDiv:
            self.mainUrl = urljoin(
                self.ORIGIN, firstDiv.find("a", href=True)["href"].strip()
            )
            return True

        return False

    def chaptersInsideReadingList(self) -> None:
        """
        Correctly set the chapterLinks after finding the reading list.

        Args:
            - None

        Returns:
            - None
        """
        self.driver.get(self.mainUrl)
        time.sleep(2)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        # Iterate across li with data-value attribute
        for li in soup.find("div", class_="mr-2 ml-2 flex-grow").find_all(
            "li", attrs={"data-value": True}
        ):
            url = urljoin(self.ORIGIN, "chapter/" + li["data-value"].strip())
            self.chapterLinks.append(url)

        # Reverse the chapter links to have them in order
        self.chapterLinks.reverse()

        # The first chapter is the main url
        if self.chapterLinks:
            self.mainUrl = self.chapterLinks[0]

    def getChapterImages(self, chapterUrl: str) -> list[str]:
        # TODO
        return []
