import Utils
import FileHandling
import os

manga = "Berserk"
minimum = "Episode"
division = "Volume"

naming = {"Episode":{"inversion":False,"numeration":False},
          "Title":{"inversion":False,"numeration":True},
          "Volume":{"inversion":False,"numeration":False},
          "Chapter":{"inversion":True,"numeration":False},
          "Arc":{"inversion":True,"numeration":False}}



image_folder = "." + manga + "JPG"
enumeration = manga + "Numeration.csv"
pdfFolder = manga + " PDF"


FileHandling.decompressZip(image_folder)

enumeration = FileHandling.openCsv(enumeration)
images = FileHandling.getImages(image_folder)
divide = Utils.divider(images,enumeration,division,minimum)


namesPdf = []
[namesPdf.append(x) for x in enumeration[division] if x not in namesPdf]

for i in divide:
    name = "Berserk PDF/Berserk "+division+" "+str(divide.index(i)+1)+ " " + namesPdf[divide.index(i)]   +".pdf"
    name = Utils.nameCreator(manga,division,namesPdf[divide.index(i)],naming[division]["inversion"],divide.index(i)+1,naming[division]["numeration"],".pdf")
    Utils.convert_images_to_pdf(image_folder, i[::-1], os.path.join(pdfFolder, name))

FileHandling.zipAndDelete(image_folder)

quit()
