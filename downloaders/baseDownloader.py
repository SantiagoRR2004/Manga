from abc import ABC, abstractmethod


class BaseDownloader(ABC):

    def __init__(self, manga: str):
        """
        Initializes the BaseDownloader with the name of the manga to be downloaded.

        Args:
            - manga (str): The name of the manga to be downloaded.

        Returns:
            - None
        """
        self.manga = manga

    @abstractmethod
    def getNumberOfChapters(self) -> int:
        """
        This funtion return the number of chapters
        of the web that were found.

        The implementation must also set:
            - self.foundName
            - self.mainUrl
            - self.chapterLinks

        Args:
            - None

        Returns:
            - int: The number of chapters that the manga has.
        """
        pass
