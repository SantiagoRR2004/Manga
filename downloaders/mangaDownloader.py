from modules import CsvHandling
import os


class MangaDownloader:
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
            Warning("Enumeration file not found.")
            return 0

        enumeration = CsvHandling.openCsv(enumerationFile)

        return max(len(x) for x in enumeration.values())
