from Modules import Internet
import os

directory = os.path.dirname(os.path.abspath(__file__))

manga = "Berserk"
maxDownload = 1
minimum = 1

Internet.mangasee123Downloader(manga,minimum,maxDownload,directory)