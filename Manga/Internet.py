from modules import FileHandling, zipping, Internet
from bs4 import BeautifulSoup
import requests
import random
import time
import os


def mangasee123UrlsXML(web):
    r = requests.get(web)
    page = BeautifulSoup(r.content, "xml")
    urls = [item.find("link").text for item in page.find_all("item")]
    return urls[::-1]

def mangasee123Downloader(
    manga, chapter, maxDownload, callerDirectory, skip=[], missing=[]
):
    mangaSpaces = manga.replace(" ", "")
    mangaHyphens = manga.replace(" ", "-")

    infofile = os.path.join(callerDirectory, "Manga.json")
    mangaData = FileHandling.openJson(infofile)

    if mangaData.get(mangaSpaces):
        if mangaData.get(mangaHyphens).get("skip"):
            skip = mangaData[mangaHyphens]["skip"]
        if mangaData.get(mangaHyphens).get("missing"):
            missing = mangaData[mangaHyphens]["missing"]

    web = "https://mangasee123.com/rss/" + mangaHyphens + ".xml"
    folder = os.path.join(callerDirectory, "." + mangaSpaces + "JPG")
    urls = mangasee123UrlsXML(web)

    for x in skip:
        if x in urls:
            urls.remove(x)

    for x in missing:
        urls.insert(x - 1, "missing")

    if len(urls) < maxDownload:
        print("There aren't that many chapters")
        maxDownload = len(urls)

    if len(urls) < chapter:
        print("The starting chapter is too high")
        chapter = len(urls)

    if chapter < 1:
        print("The starting chapter can't be less than 1")
        chapter = 1

    if maxDownload < 1:
        print("The last chapter can't be less than 1")
        maxDownload = 1

    FileHandling.ensureExistance(folder)
    driver = Internet.configureChrome()

    while chapter <= maxDownload:
        if chapter in missing:
            pass

        else:
            driver.get(urls[chapter - 1])
            Internet.clickButton(driver, "Long Strip")

            png_image_urls = Internet.findPNGs(driver)

            for i in range(len(png_image_urls)):
                name = (
                    str(chapter) + "{:0>{}}".format(i, 3) + ".jpg"
                )  # Try to change it to png
                Internet.downloadImage(png_image_urls[i], os.path.join(folder, name))

        print("Se ha descargado el capítulo " + str(chapter))
        chapter += 1
        time.sleep(random.uniform(1, 10))

    driver.quit()

    zipping.zipAndDelete(folder)
