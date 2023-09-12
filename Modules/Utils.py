import requests
import os
from PIL import Image
import PyPDF2
from reportlab.pdfgen import canvas
import os
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
                segment.extend([x for x in images if int(x[:-7])==int(classifier[minimum][j])])

        toret.append(segment)
    return toret


def convert_images_to_pdf(image_folder,imageList, output_pdf,temporalFolder = ".TemporalPdf"):
    if not os.path.isdir(temporalFolder):
        os.mkdir(temporalFolder)
    else:
        emptyFolder(temporalFolder)

    pdf_writer = PyPDF2.PdfWriter()
    smallerPdfs = []

    cover = Image.open(os.path.join(image_folder, imageList[0]))
    width =  cover.width

    for image_file in imageList:
        image_path = os.path.join(image_folder, image_file)

        # Open each image file using PIL
        image = Image.open(image_path)
        pageNumber = round(image.width/width)

        for i in range(pageNumber): # Number of pages in width
            
            fileName = ".TemporalPdf/"+image_file[:-4]+str(i)+".pdf"
            
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

    for filename in os.listdir(temporalFolder):
        os.remove(os.path.join(temporalFolder,filename))


    print(output_pdf+" created successfully!")

