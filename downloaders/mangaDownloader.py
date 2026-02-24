from .mangafireDownloader import MangaFireDownloader
from .mangaboltDownloader import MangaboltDownloader
from .baseDownloader import BaseDownloader
from modules import CsvHandling
import logging
import os


class MangaDownloader:
    DOWNLOADERS: list[BaseDownloader] = [MangaFireDownloader, MangaboltDownloader]

    def __init__(self, mangaName: str, mangaDirectory: str) -> None:
        """
        Initializes the MangaDownloader with the name of the manga and the directory
        where the manga data is meant to be stored.

        Args:
            - mangaName (str): The name of the manga (no problem with spaces).
            - mangaDirectory (str): The directory where the manga data is meant to be stored.

        Returns:
            - None
        """
        self.manga = mangaName
        self.directory = mangaDirectory

        self.minChapters = self.getMinimumChapters()

        # Check which downloaders work
        self.valid = []
        for downloader in self.DOWNLOADERS:
            d: BaseDownloader = downloader(mangaName)
            d.findChapters()
            if len(d.chapterLinks) >= self.minChapters:
                self.valid.append(d)
            else:
                logging.warning(f"{downloader.__name__} does not have enough chapters.")

    def getMinimumChapters(self) -> int:
        """
        Returns the minimum number of chapter that the numeration has.
        This number is important because the web will be required to have
        more than this number of chapters to be able to download the manga.

        Args:
            - None

        Returns:
            - int: The minimum number of chapter that the numeration has.
        """
        enumerationFile = os.path.join(
            self.directory, f"{self.manga.replace(' ', '')}Numeration.csv"
        )

        # Check it exists
        if not os.path.exists(enumerationFile):
            logging.warning("Enumeration file not found.")
            return 0

        enumeration = CsvHandling.openCsv(enumerationFile)

        return max(len(x) for x in enumeration.values())
