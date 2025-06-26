from Modules import FileHandling
from Modules import zipping
from Modules import Internet
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, urlunparse

# https://mangaclash.com/manga/jojos-bizarre-adventure/chapter-1/


webs = [
    "https://readjojos.com/chapter/jojos-bizarre-adventure-part-1-phantom-blood-chapter-1/",
    "https://readjojos.com/chapter/jojos-bizarre-adventure-part-2-battle-tendency-chapter-1/",
    "https://readjojos.com/chapter/jojos-bizarre-adventure-part-3-stardust-crusaders-chapter-1/",
    "https://readjojos.com/chapter/jojos-bizarre-adventure-part-4-diamond-is-unbreakable-chapter-1/",
    "https://readjojos.com/chapter/jojos-bizarre-adventure-part-5-golden-wind-chapter-1/",
    "https://readjojos.com/chapter/jojos-bizarre-adventure-part-6-stone-ocean-chapter-1/",
    "https://readjojos.com/chapter/jojo-no-kimyou-na-bouken-part-7-steel-ball-run-chapter-1/",
    "https://readjojos.com/chapter/jojos-bizarre-adventure-part-8-jojolion-chapter-1/",
    "https://readjojos.com/chapter/jojo-no-kimyou-na-bouken-part-9-the-jojolands-chapter-1/",
]
folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".JoJoJPG")

# Start and end of the chapters to download
chapter = 1
maxDownload = 297

# Get all the URLs of the chapters
urls = []
for web in webs:
    r = requests.get(web)
    page = BeautifulSoup(r.content, "html.parser")
    urls.extend(
        [x["value"] for x in (page.find_all("select")[0]).find_all("option")][::-1]
    )

# Eliminate urls that end with /
urls = [url for url in urls if not url.endswith("/")]

# Ensure there are enough URLs to download
chapter = max(1, chapter)
maxDownload = min(maxDownload, len(urls))

FileHandling.ensureExistance(folder)

while chapter <= maxDownload:

    r = requests.get(urls[chapter - 1])
    page = BeautifulSoup(r.content, "html.parser")
    images = page.find_all(class_="text-center")

    for i in images:
        if i.img is not None:
            imageUrl = urlunparse(urlparse(i.img["src"])._replace(query=""))
            if imageUrl.endswith(".jpg"):
                name = str(chapter * 1000 + int(imageUrl.split("/")[-1][:-4])) + ".jpg"
            elif imageUrl.endswith(".jpeg"):
                name = str(chapter * 1000 + int(imageUrl.split("/")[-1][:-5])) + ".jpeg"
            Internet.downloadImage(i.img["src"], os.path.join(folder, name))

    print("Se ha descargado el capítulo " + str(chapter))

    chapter += 1

zipping.zipAndDelete(folder)
