from Modules import FileHandling
from Modules import zipping
from Modules import Internet
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, urlunparse
import tqdm

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
maxDownload = 900

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
width = len(str(maxDownload))

FileHandling.ensureExistance(folder)

while chapter <= maxDownload:

    r = requests.get(urls[chapter - 1])
    page = BeautifulSoup(r.content, "html.parser")
    images = [i for i in page.find_all(class_="text-center") if i.img is not None]

    for i in tqdm.tqdm(images, desc=f"Capítulo {chapter:0{width}d}"):

        imageUrl = urlunparse(urlparse(i.img["src"])._replace(query=""))
        name = None

        formats = [".png", ".jpg", ".jpeg"]
        for f in formats:
            if imageUrl.endswith(f):
                number = imageUrl.split("/")[-1][: -len(f)]
                if number.isdigit() is True:
                    name = str(chapter * 1000 + int(number)) + f

        if name is not None:
            Internet.downloadImage(i.img["src"].strip(), os.path.join(folder, name))

    chapter += 1

zipping.zipAndDelete(folder)
