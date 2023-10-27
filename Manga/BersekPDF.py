from Modules import Utils
from Modules import FileHandling
from Modules import zipping
import os

directory = os.path.dirname(os.path.abspath(__file__))
manga = "Berserk"
minimum = "Episode"
division = "Volume"

naming = {"Episode":{"inversion":False,"numeration":False},
          "Title":{"inversion":False,"numeration":True},
          "Volume":{"inversion":False,"numeration":False},
          "Chapter":{"inversion":True,"numeration":False},
          "Arc":{"inversion":True,"numeration":False}}


image_folder = os.path.join(directory,"." + manga + "JPG")
enumeration = os.path.join(directory,manga + "Numeration.csv")
pdfFolder = os.path.join(directory,manga + " PDF")


FileHandling.ensureExistance(image_folder)
FileHandling.ensureExistance(pdfFolder)

enumeration = FileHandling.openCsv(enumeration)
images = FileHandling.findPatternFolder(image_folder,".jpg$")
divide = Utils.divider(images,enumeration,division,minimum)


namesPdf = []
[namesPdf.append(x) for x in enumeration[division] if x not in namesPdf]

for i in divide:
    name = "Berserk PDF/Berserk "+division+" "+str(divide.index(i)+1)+ " " + namesPdf[divide.index(i)]   +".pdf"
    name = Utils.nameCreator(manga,division,namesPdf[divide.index(i)],naming[division]["inversion"],divide.index(i)+1,naming[division]["numeration"],".pdf")
    Utils.convert_images_to_pdf(image_folder, i[::-1], os.path.join(pdfFolder, name))

zipping.zipAndDelete(image_folder)

quit()
