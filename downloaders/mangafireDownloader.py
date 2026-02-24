from .baseDownloader import BaseDownloader
import requests


class MangaFireDownloader(BaseDownloader):

    def getNumberOfChapters(self) -> int:
        """
        I tried using a web driver, but it keeps reloading.
        The only option is to have the exact name of the manga.

        Args:
            - None

        Returns:
            - int: The number of chapters of the manga.
        """
        url = "https://mangafire.to/manga/" + self.manga.replace(" ", "-")
        response = requests.get(url)

        if response.status_code == 200:
            print("Sorprisingly, the manga can be found in MangaFire.")

        return 0
