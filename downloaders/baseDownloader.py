from abc import ABC, abstractmethod


class BaseDownloader(ABC):

    chapterLinks: list[str]
    foundName: str
    mainUrl: str

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
    def findChapters(self) -> None:
        """
        This funtion needs store the a list of the urls
        of each chapter of the manga as set self.chapterLinks.
        If nothing is found, self.chapterLinks should be an empty list.

        If len(self.chapterLinks) > 0 it must also set:
            - self.foundName
            - self.mainUrl

        Args:
            - None

        Returns:
            - None
        """
        pass

    @abstractmethod
    def getChapterImages(self, chapterUrl: str) -> list[str]:
        """
        This function needs to return a list of the urls of
        the images of the chapter given by chapterUrl.

        Args:
            - chapterUrl (str): The url of the chapter.

        Returns:
            - list[str]: A list of the urls of the images of the chapter.
        """
        pass
