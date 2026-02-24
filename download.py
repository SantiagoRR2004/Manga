from downloaders import MangaDownloader
import os

if __name__ == "__main__":
    # The start and end of chapters to download
    start = 0
    maxDownload = 10

    currentDirectory = os.path.dirname(os.path.abspath(__file__))
    downloader = MangaDownloader("Berserk", os.path.join(currentDirectory, "Manga"))
    downloader.downloadChapters(start, maxDownload)
