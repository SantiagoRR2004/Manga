from .baseDownloader import BaseDownloader
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import difflib
import re


class MangaboltDownloader(BaseDownloader):

    ORIGIN = "https://mangabolt.com/"

    def findChapters(self) -> None:

        # Initial empty list
        self.chapterLinks = []

        # Get the html with the list of mangas
        url = urljoin(self.ORIGIN, "storage/manga-list.html")
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            # Find all the divs with class two-column-layout
            mangaListDiv = soup.find_all("div", class_="two-column-layout")

            mangaLinks = {}

            # Need to find item-title or h2 close to the onclick
            for mangaList in mangaListDiv:
                for entry in mangaList.find_all(attrs={"onclick": True}):
                    onclick = entry.get("onclick", "")
                    match = re.search(r"location\.href=['\"]([^'\"]+)['\"]", onclick)

                    href = urljoin(self.ORIGIN, match.group(1))
                    title_tag = entry.find("h2") or entry.find(
                        "span", class_="item-title"
                    )

                    title = title_tag.get_text(strip=True)
                    if title:
                        mangaLinks[title] = href

            self.foundName = max(
                mangaLinks,
                key=lambda k: difflib.SequenceMatcher(None, k, self.manga).ratio(),
            )
            self.mainUrl = urljoin(self.ORIGIN, mangaLinks[self.foundName])

            response2 = requests.get(self.mainUrl)

            if response2.status_code == 200:
                soup2 = BeautifulSoup(response2.content, "html.parser")

                # All links from main with id main-content
                mainContent = soup2.find(id="main-content")
                chapterLinks = mainContent.find_all("a", href=True)

                # Invert to have the correct order
                self.chapterLinks = [
                    urljoin(self.ORIGIN, link["href"]) for link in chapterLinks
                ][::-1]
