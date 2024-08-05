from Modules import Utils
from Modules import FileHandling
from Modules import zipping
from Modules import Internet
import requests
from bs4 import BeautifulSoup
import os

# https://mangaclash.com/manga/jojos-bizarre-adventure/chapter-1/


maxChapter = 371+16
maxDownload = 150
web = "https://readberserk.com/manga/berserk-chapter-1/"
chapter = 50
folder = ".BerserkJPG"
skip = ["https://readberserk.com/manga/berserk-chapter-99-5/","https://readberserk.com/manga/berserk-chapter-350-5/"]

r = requests.get(web)
print(r)
page = BeautifulSoup(r.content, 'html.parser')
print(page)
urls = [x["value"] for x in (page.find_all("select")[0]).find_all("option")][::-1]

for x in skip:
    if x in urls:
        urls.remove(x)

urls.insert(98,"missing")

FileHandling.ensureExistance(folder)


while chapter <= maxDownload:
    
    if chapter == 45:
        numberPages = 17
        web2 = "https://cdn.berserkmanga.net/file/mangap/1/20029000/{0}.jpg"
        for i in range(numberPages):
            name = str(chapter*1000 + (i+1)) + ".jpg"
            Utils.download_image(web2.format(i+1), os.path.join(folder,name))
            
    elif chapter == 118:
        numberPages = 21
        web2 = "https://cdn.berserkmanga.net/file/mangap/1/20102000/{0}.jpg"
        for i in range(numberPages):
            name = str(chapter*1000 + (i+1)) + ".jpg"
            Utils.download_image(web2.format(i+1), os.path.join(folder,name))

    elif chapter == 99:# This chapter isn't canonical and in the  web
        pass

    

    else:
        
        r = requests.get(urls[chapter-1])
        page = BeautifulSoup(r.content, 'html.parser')
        images = page.find_all(class_="img_container")
        
        for i in images:
            name = str(chapter*1000 + int(i.img["src"].split('/')[-1][:-4])) + ".jpg"
            Internet.downloadImage(i.img["src"], os.path.join(folder,name))
    
    print("Se ha descargado el capítulo "+str(chapter))
    chapter += 1
##    print(urls[chapter-1])

zipping.zipAndDelete(folder)

quit()

