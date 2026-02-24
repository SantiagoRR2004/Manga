from .baseDownloader import BaseDownloader
import requests


class MangaFireDownloader(BaseDownloader):

    def findChapters(self) -> None:
        """
        I tried using a web driver, but it keeps reloading.
        The only option is to have the exact name of the manga.

        Args:
            - None

        Returns:
            - None
        """
        url = "https://mangafire.to/manga/" + self.manga.replace(" ", "-")
        response = requests.get(url)

        if response.status_code == 200:
            print("Sorprisingly, the manga can be found in MangaFire.")

        self.chapterLinks = []

    def getChapterImages(self, chapterUrl: str) -> list[str]:
        return []
