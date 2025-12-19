from Modules import FileHandling
from Modules import zipping
from Modules import Internet
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, urlunparse
import tqdm

# https://w37.read-attackontitan-manga.com/manga/attack-on-titan-chapter-1/
# https://toonclash.com/manga/attack-on-titan/chapter-1/

folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".AttackOnTitanJPG")

# Start and end of the chapters to download
chapter = 1
maxDownload = 150

web = "https://w37.read-attackontitan-manga.com/"
r = requests.get(web)
page = BeautifulSoup(r.content, "html.parser")

# Find the class="widget ceo_latest_comics_widget"
urlSection = page.find(
    class_=["widget ceo_latest_comics_widget"], id="ceo_latest_comics_widget-3"
)

# Find all the hrefs in the urlSection
urls = [x["href"] for x in urlSection.find_all("a") if x.get("href") is not None]

# Reverse the order of the urls
urls = urls[::-1]

# Ensure there are enough URLs to download
chapter = max(1, chapter)
maxDownload = min(maxDownload, len(urls))
width = len(str(maxDownload))

FileHandling.ensureExistance(folder)

while chapter <= maxDownload:

    r = requests.get(urls[chapter - 1])
    print(urls[chapter - 1])
    page = BeautifulSoup(r.content, "html.parser")
    images = [i for i in page.find_all(class_="separator") if i.img is not None]

    if not images:
        images = [
            i for i in page.find_all(class_="page-break no-gaps") if i.img is not None
        ]

    for i in tqdm.tqdm(images, desc=f"Capítulo {chapter:0{width}d}"):

        # The image is in data-lazy-src attribute
        if "data-lazy-src" in i.img.attrs:
            image = i.img["data-lazy-src"]
        else:
            image = i.img["src"]

        imageUrl = urlunparse(urlparse(image)._replace(query=""))
        name = None

        formats = [".png", ".jpg", ".jpeg"]
        for f in formats:
            if imageUrl.endswith(f):
                number = imageUrl.split("/")[-1][: -len(f)]
                if number.isdigit() is True:
                    name = str(chapter * 1000 + int(number)) + f

        if name is not None:
            Internet.downloadImage(image.strip(), os.path.join(folder, name))

    chapter += 1

zipping.zipAndDelete(folder)
