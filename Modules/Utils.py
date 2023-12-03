import os
from PIL import Image
import os
import zipfile
from Modules import FileHandling
from Modules import CsvHandling
from Modules import zipping

def divider(images,classifier,key,minimum):
    toret = []
    my_list = [x for i, x in enumerate(classifier[key]) if x not in classifier[key][:i]]
    if None in my_list:
        my_list.remove(None)

    for i in my_list:
        segment = []
        for j in range(len(classifier[key])):
            if classifier[key][j] == i:
                segment.extend([x for x in images if x[:-7]==classifier[minimum][j]])
        toret.append(segment)
    return toret

def create_cbz(images_folder, imagesList, output_cbz,temporalFolder = ".Temporal"):

    FileHandling.ensureExistance(temporalFolder)
    if sorted(imagesList) != imagesList:
        for image_file in imagesList: 
            FileHandling.copyFile(images_folder,image_file,temporalFolder,str(imagesList.index(image_file))+".jpg")
        images_folder = temporalFolder
        imagesList = FileHandling.findPatternFolder(temporalFolder,".jpg$")

    with zipfile.ZipFile(output_cbz, 'w', zipfile.ZIP_DEFLATED) as cbz:
        for image_file in imagesList:
            image_path = os.path.join(images_folder, image_file)
            with Image.open(image_path) as img: # Does this do anything?
                #rgb_image = img.convert("RGB")
                cbz.write(image_path, arcname=os.path.basename(image_path))

    FileHandling.deleteFolder(temporalFolder)


    print(output_cbz+" created successfully!")

def nameCreator(manga,division,name,inversion:bool,number,numeration:bool,format):
    if numeration:
        middle = division + " " + str(number)
    else:
        middle = division

    if inversion:
        middle = name + " " + middle
    else:
        middle = middle + " " + name

    return manga  + " " + middle + format
    
def preparationForCBZ(manga,minimum,callerDirectory,division,naming):
    image_folder = os.path.join(callerDirectory,"." + manga + "JPG")
    enumeration = os.path.join(callerDirectory,manga + "Numeration.csv")
    pdfFolder = os.path.join(callerDirectory,manga + " CBZ")

    FileHandling.ensureExistance(image_folder)
    FileHandling.ensureExistance(pdfFolder)

    enumeration = CsvHandling.openCsv(enumeration)
    images = FileHandling.findPatternFolder(image_folder,".jpg$")
    divide = divider(images,enumeration,division,minimum)

    names = []
    [names.append(x) for x in enumeration[division] if x not in names]

    for i in divide:
        name = nameCreator(manga,division,names[divide.index(i)],naming[division]["inversion"],divide.index(i)+1,naming[division]["numeration"],".cbz")
        create_cbz(image_folder, i[::-1], os.path.join(pdfFolder, name))

    zipping.zipAndDelete(image_folder)

