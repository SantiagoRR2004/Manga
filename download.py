from downloaders import MangaDownloader
import os

if __name__ == "__main__":
    currentDirectory = os.path.dirname(os.path.abspath(__file__))
    downloader = MangaDownloader("Berserk", os.path.join(currentDirectory, "Manga"))
