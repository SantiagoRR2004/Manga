import requests
import os
from PIL import Image
import PyPDF2
from reportlab.pdfgen import canvas
import os
from Modules import FileHandling
#https://stackoverflow.com/questions/44375872/pypdf2-returning-blank-pdf-after-copy

def deleteFolder(path):
    emptyFolder(path)
    os.removedirs(path)

def emptyFolder(path):
    for filename in os.listdir(path):
            if os.path.isdir(os.path.join(path,filename)):
                deleteFolder(path)
            else:
                os.remove(os.path.join(path,filename))

def download_image(url, dest_file):
    if not os.path.isfile(dest_file):
        response = requests.get(url)
        if response.status_code == 200:
            with open(dest_file, 'wb') as f:
                f.write(response.content)

def get_images(image_folder):
    # Get a list of all JPEG files in the specified folder
    image_files = [f for f in os.listdir(image_folder) if f.endswith(".jpg")]
    numbers = [int(x[:-4]) for x in image_files]
    image_files = [x for _,x in sorted(zip(numbers,image_files))]
    return image_files


def divider(images,classifier,key,minimum):
    toret = []
    my_list = [x for i, x in enumerate(classifier[key]) if x not in classifier[key][:i]]
    for i in my_list:
        segment = []
        for j in range(len(classifier[key])):
            if classifier[key][j] == i:
                segment.extend([x for x in images if x[:-7]==classifier[minimum][j]])
        toret.append(segment)
    return toret

def convert_images_to_pdf(image_folder,imageList, output_pdf,temporalFolder = ".Temporal"):
    FileHandling.ensureExistance(temporalFolder)

    pdf_writer = PyPDF2.PdfWriter()
    smallerPdfs = []


    if not imageList:
        FileHandling.deleteFolder(temporalFolder)
        print("Can't create "+output_pdf) 
        return False

    cover = Image.open(os.path.join(image_folder, imageList[0]))
    width =  cover.width

    for image_file in imageList:
        image_path = os.path.join(image_folder, image_file)

        # Open each image file using PIL
        image = Image.open(image_path)
        pageNumber = round(image.width/width)

        for i in range(pageNumber): # Number of pages in width
            
            fileName = temporalFolder+"/"+image_file[:-4]+str(i)+".pdf"
            
            pdf_page = canvas.Canvas(fileName, pagesize=(width, image.height))
            pdf_page.drawImage(image_path, -i*width, 0, width=image.width, height=image.height)
            pdf_page.showPage()
            pdf_page.save()
            
            # We open the pdfs manually so empty pages don't appear
            smallerPdfs.append(PyPDF2.PdfReader(open(fileName,"rb")))
            # We don't close the pdfs manually

    for pdf in smallerPdfs:
       pdf_writer.add_page(pdf.pages[0])
       
    # Save the resulting PDF to the specified output path
    with open(output_pdf, 'wb') as output:
        pdf_writer.write(output)

    FileHandling.deleteFolder(temporalFolder)

    print(output_pdf+" created successfully!")

def create_cbz(images_folder, imagesList, output_cbz,temporalFolder = ".Temporal"):

    FileHandling.ensureExistance(temporalFolder)
    if sorted(imagesList) != imagesList:
        for image_file in imagesList: 
            FileHandling.copyFile(images_folder,image_file,temporalFolder,str(imagesList.index(image_file))+".jpg")
        images_folder = temporalFolder
        imagesList = FileHandling.getImages(temporalFolder)

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

    enumeration = FileHandling.openCsv(enumeration)
    images = FileHandling.getImages(image_folder)
    divide = divider(images,enumeration,division,minimum)

    names = []
    [names.append(x) for x in enumeration[division] if x not in names]

    for i in divide:
        name = nameCreator(manga,division,names[divide.index(i)],naming[division]["inversion"],divide.index(i)+1,naming[division]["numeration"],".cbz")
        create_cbz(image_folder, i[::-1], os.path.join(pdfFolder, name))

    FileHandling.zipAndDelete(image_folder)

