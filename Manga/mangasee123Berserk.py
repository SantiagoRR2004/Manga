import Internet


manga = "Berserk"
maxDownload = 400
minimum = 350
skip = ["https://mangasee123.com/read-online/Berserk-chapter-99.5-index-2-page-1.html",
        "https://mangasee123.com/read-online/Berserk-chapter-350.5-index-2-page-1.html"]
missing = [99]

Internet.mangasee123Downloader(manga,minimum,maxDownload,skip,missing)

quit()
