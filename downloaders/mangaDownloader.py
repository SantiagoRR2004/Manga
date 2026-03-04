from modules import CsvHandling, FileHandling, Internet, zipping
from .baseDownloader import BaseDownloader
from urllib.parse import urlparse
import downloaders
import logging
import tqdm
import os


class MangaDownloader:
    DOWNLOADERS = downloaders.DOWNLOADERS
    FORMATS = [".png", ".jpg", ".jpeg"]

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
        self.imageDirectory = os.path.join(
            mangaDirectory, "." + mangaName.replace(" ", "") + "JPG"
        )

        self.minChapters = self.getMinimumChapters()

        # Check which downloaders work
        self.valid: list[BaseDownloader] = []
        for downloader in self.DOWNLOADERS:
            d = downloader(mangaName)
            d.findChapters()
            if len(d.chapterLinks) >= self.minChapters:
                self.valid.append(d)
            else:
                logging.warning(f"{downloader.__name__} does not have enough chapters.")

        # If no downloader is valid, print a warning
        if not self.valid:
            logging.warning("No downloader found with enough chapters.")
            return

        self.chosenDownloader: BaseDownloader = None

        if len(self.valid) > 1:

            # Make the user choose
            while not self.chosenDownloader:
                print("Multiple downloaders found:")

                for i, downloader in enumerate(self.valid, 1):
                    print(f'[{i}] "{downloader.foundName}" ({downloader.mainUrl})')

                choice = input("Choose a downloader by number: ")

                if choice.isdigit() and 1 <= int(choice) <= len(self.valid):
                    self.chosenDownloader = self.valid[int(choice) - 1]
                else:
                    print("Invalid choice. Please try again.")

        else:
            self.chosenDownloader = self.valid[0]

    def getMinimumChapters(self) -> int:
        """
        Returns the minimum number of chapter that the enumeration has.
        This number is important because the web will be required to have
        more than this number of chapters to be able to download the manga.

        Args:
            - None

        Returns:
            - int: The minimum number of chapter that the enumeration has.
        """
        enumerationFile = os.path.join(
            self.directory, f"{self.manga.replace(' ', '')}Enumeration.csv"
        )

        # Check it exists
        if not os.path.exists(enumerationFile):
            logging.warning("Enumeration file not found.")
            return 0

        enumeration = CsvHandling.openCsv(enumerationFile)

        return max(len(x) for x in enumeration.values())

    def downloadChapters(self, start: int = 1, maxDownload: int = None) -> None:
        """
        Downloads the chapters of the manga using the chosen downloader.

        Args:
            - start (int): The starting chapter number, default is to start
                from the first chapter.
            - maxDownload (int): The maximum number of chapters to download,
                default is to download all the chapters.

        Returns:
            - None
        """
        # Ensure the image directory exists
        FileHandling.ensureExistance(self.imageDirectory)

        # Ensure there are enough URLs to download
        start = max(1, start)

        if maxDownload:
            maxDownload = min(maxDownload, len(self.chosenDownloader.chapterLinks))
        else:
            maxDownload = len(self.chosenDownloader.chapterLinks)

        width = len(str(maxDownload))

        for chapter, chapterLink in enumerate(
            self.chosenDownloader.chapterLinks[start - 1 : maxDownload], start
        ):

            # Get the images
            images = self.chosenDownloader.getChapterImages(chapterLink)

            for n, img in tqdm.tqdm(
                enumerate(images, 1),
                desc=f"Chapter {chapter:0{width}d}",
                total=len(images),
            ):

                path = urlparse(img).path

                name = None
                for f in self.FORMATS:
                    if path.endswith(f):
                        # No chapter should have more than 1000 pages
                        name = str(chapter * 1000 + n) + f
                        break

                if name:
                    Internet.downloadImage(
                        img,
                        os.path.join(self.imageDirectory, name),
                        headers={"Referer": chapterLink},
                    )

        zipping.zipAndDelete(self.imageDirectory)
