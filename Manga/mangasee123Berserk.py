from Modules import Internet
import os

directory = os.path.dirname(os.path.abspath(__file__))

manga = "Berserk"
maxDownload = 1
minimum = 1
skip = ["https://mangasee123.com/read-online/Berserk-chapter-99.5-index-2-page-1.html",
        "https://mangasee123.com/read-online/Berserk-chapter-350.5-index-2-page-1.html"]
missing = [99]

Internet.mangasee123Downloader(manga,minimum,maxDownload,directory,skip,missing)

quit()
