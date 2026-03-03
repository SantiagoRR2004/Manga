from modules import FileHandling, zipping
from reportlab.pdfgen import canvas
from collections import Counter
from typing import List, Dict
from PIL import Image
import pandas as pd
import logging
import PyPDF2
import os


class MangaCreator:
    temporalFolder = ".Temporal"

    def __init__(self, mangaName: str, callerDirectory: str) -> None:
        """
        Initializes the MangaCreator with the name of the manga and the directory
        with all the data.

        Args:
            - mangaName (str): The name of the manga (no problem with spaces).
            - callerDirectory (str): The directory where the manga data is stored.

        Returns:
            - None
        """
        self.manga = mangaName
        self.callerDirectory = callerDirectory
        self.enumeration = self.getEnumeration()

        imageFolder = os.path.join(
            self.callerDirectory, "." + self.manga.replace(" ", "") + "JPG"
        )
        self.imageFolder = imageFolder
        FileHandling.ensureExistance(imageFolder)
        self.images = sorted(os.listdir(imageFolder))

    def getEnumeration(self) -> pd.DataFrame:
        """
        Reads the enumeration file for the manga and returns its content as a dictionary.

        It also saves the minimum key for later use.

        Args:
            - None

        Returns:
            - pd.DataFrame: The enumeration DataFrame.
        """
        enumerationFile = os.path.join(
            self.callerDirectory, self.manga.replace(" ", "") + "Numeration.csv"
        )
        if not os.path.exists(enumerationFile):
            logging.warning("Enumeration file not found.")
            return

        enumeration = pd.read_csv(enumerationFile)

        # Store the minimum for later use
        self.minimum = self.getMinimum(enumeration)

        return enumeration

    def getMinimum(self, enumeration: pd.DataFrame) -> str:
        """
        Search for the first unique key in the enumeration DataFrame.

        Args:
            - enumeration (pd.DataFrame): The enumeration DataFrame.

        Returns:
            - str: The first key with unique values in its column.
        """
        for key in enumeration.columns:
            if len(set(enumeration[key])) == len(enumeration[key]):
                return key

    def createFiles(self, division: str = None, extension: str = "CBZ") -> None:
        """
        Creates the files for the manga based on the specified division and extension.

        If there is no enumeration or the division is not given, it defaults to "Chapter".

        Args:
            - division (str): The division to use for creating the files.
            - extension (str): The extension of the files to create (PDF, CBZ, ZIP).

        Returns:
            - None
        """
        methodName = f"create{extension.upper()}"
        method = getattr(self, methodName, None)
        self.division = division

        # Check if the method exists and is callable
        if not callable(method):
            raise ValueError(f"Unsupported extension: {extension}")

        # Check if the division exists in the enumeration
        if (
            self.enumeration is not None
            and self.division not in self.enumeration.columns
        ):
            raise ValueError(f"Division '{self.division}' not found in enumeration.")

        elif self.enumeration is None:
            # Use Chapter ad default division if no enumeration is provided
            logging.warning("Using 'Chapter' as default division.")
            self.division = "Chapter"

        elif self.division is None:
            # Use the minimum instead
            logging.warning(f"Using '{self.minimum}' as division.")
            self.division = self.minimum

        finalFolder = os.path.join(
            self.callerDirectory, self.manga.replace(" ", "") + " " + extension.upper()
        )
        FileHandling.ensureExistance(finalFolder)

        dividedImages = self.divider()
        names = {
            ogName: n + "." + extension.lower()
            for ogName, n in self.getNames(dividedImages).items()
        }

        # Create the temporal folder if it doesn't exist
        FileHandling.ensureExistance(self.temporalFolder)

        for ogName, segment in dividedImages.items():

            # Check if the segment is empty
            if not segment:
                print(f"No images found for '{names[ogName]}'.")
            else:
                fileName = os.path.join(finalFolder, names[ogName])

                try:
                    method(segment, fileName)
                    print(f"{fileName} created successfully!")
                except Exception as e:
                    print(f"Error creating {names[ogName]}: {e}")

        # Clean up
        zipping.zipAndDelete(self.imageFolder)
        FileHandling.deleteFolder(self.temporalFolder)

    def divider(self) -> Dict[str, List[str]]:
        """
        Divides the images based on the unique values in the specified division.

        Returns:
            - Dict[str, List[str]]: A dictionary where keys are unique values in
                the division and values are lists of images corresponding to each unique value.
        """
        # Precompute image markers
        imageMap = {"".join(image.split(".")[:-1])[:-3]: [] for image in self.images}

        for image in self.images:
            marker = "".join(image.split(".")[:-1])  # Remove the extension
            marker = marker[:-3]  # No more than 999 images
            imageMap[marker].append(image)

        # If no enumeration, use map directly
        if self.enumeration is None:
            return imageMap

        # Drop NaN and group by division
        grouped = self.enumeration.dropna(subset=[self.division]).groupby(
            self.division, sort=False
        )[self.minimum]

        # Build result
        toret = {
            key: [image for marker in group for image in imageMap.get(marker, [])]
            for key, group in grouped
        }

        # Unused images are added
        usedMarkers = [marker for _, group in grouped for marker in group]
        unused = {div: imgs for div, imgs in imageMap.items() if div not in usedMarkers}

        for div, imgs in unused.items():
            if not toret.get(div):
                toret[div] = imgs

        return toret

    def getNames(self, dividedImages: Dict[str, List[str]]) -> Dict[str, str]:
        """
        Returns the names of the manga based on the specified division.

        Args:
            - dividedImages (Dict[str, List[str]]): The dictionary of divided images.

        Returns:
            - Dict[str, str]: The map where keys are the unique values
                in the division and values are the corresponding names.
        """
        uniqueList = list(dividedImages.keys())

        if len(uniqueList) <= 1:
            needNumberFlag = False
        else:
            inOrder = sum(
                1
                for i in range(len(uniqueList) - 1)
                if uniqueList[i] <= uniqueList[i + 1]
            )
            total_pairs = len(uniqueList) - 1
            needNumberFlag = (inOrder / total_pairs) < 0.9

        names = {}

        for i, n in enumerate(uniqueList):
            if needNumberFlag:
                middle = self.division + " " + str(i + 1)
            else:
                middle = self.division

            middle = middle + " " + uniqueList[i]

            name = self.manga + " " + middle

            names[n] = name

        return names

    def createPDF(self, imageList: List[str], outputFile: str) -> None:
        """
        Creates a PDF file from a list of images.

        THIS IS DEPRECATED BECAUSE CALIBRE HANDLES CBZ BETTER.

        Args:
            - imageList (List[str]): List of image filenames to include in the PDF.
            - outputFile (str): The path where the output PDF will be saved.

        Returns:
            - None
        """
        # https://stackoverflow.com/questions/44375872/pypdf2-returning-blank-pdf-after-copy

        pdf_writer = PyPDF2.PdfWriter()
        smallerPdfs = []

        width = Counter(
            [Image.open(os.path.join(self.imageFolder, x)).width for x in imageList]
        ).most_common(1)[0][0]

        for image_file in imageList:
            image_path = os.path.join(self.imageFolder, image_file)

            # Open each image file using PIL
            image = Image.open(image_path)
            pageNumber = round(image.width / width)

            # Normal sized image, create PDF directly
            temp_pdf_path = os.path.join(
                self.temporalFolder, f"{os.path.splitext(image_file)[0]}.pdf"
            )
            pdf_page = canvas.Canvas(
                temp_pdf_path, pagesize=(image.width, image.height)
            )
            pdf_page.drawImage(image_path, 0, 0, width=image.width, height=image.height)
            pdf_page.showPage()
            pdf_page.save()

            smallerPdfs.append(PyPDF2.PdfReader(open(temp_pdf_path, "rb")))

            if pageNumber > 1:
                # Image is too wide, divide it into multiple pages
                base_filename = os.path.splitext(image_file)[0]
                currentWidth = image.width / pageNumber

                for i in reversed(range(pageNumber)):
                    # Create cropped image for each page
                    left = i * currentWidth
                    right = min((i + 1) * currentWidth, image.width)
                    cropped_image = image.crop((left, 0, right, image.height))

                    # Save cropped image to temporary file
                    temp_image_path = os.path.join(
                        self.temporalFolder, f"{base_filename}_{pageNumber-1-i:03d}.jpg"
                    )
                    cropped_image.save(temp_image_path)

                    # Create PDF from the cropped image
                    temp_pdf_path = os.path.join(
                        self.temporalFolder, f"{base_filename}_{pageNumber-1-i:03d}.pdf"
                    )
                    pdf_page = canvas.Canvas(
                        temp_pdf_path,
                        pagesize=(cropped_image.width, cropped_image.height),
                    )
                    pdf_page.drawImage(
                        temp_image_path,
                        0,
                        0,
                        width=cropped_image.width,
                        height=cropped_image.height,
                    )
                    pdf_page.showPage()
                    pdf_page.save()

                    # Add to the collection
                    smallerPdfs.append(PyPDF2.PdfReader(open(temp_pdf_path, "rb")))

        for pdf in smallerPdfs:
            pdf_writer.add_page(pdf.pages[0])

        # Save the resulting PDF to the specified output path
        with open(outputFile, "wb") as output:
            pdf_writer.write(output)

    def createCBZ(self, imagesList: List[str], outputFile: str) -> None:
        """
        Creates a CBZ (Comic Book Zip) file from a list of images.

        The way to properly use Calibre to create an AZW3 file is to:
            - In the "Comic input" tab, select the "Landscape" option.
                (Stops images from being split in half)
            - In the "AZW3 output" tab, select the
                "Do not add a table of contents" option.

        Args:
            - imagesList (List[str]): List of image filenames to include in the CBZ.
            - outputFile (str): The path where the output CBZ will be saved.

        Returns:
            - None
        """
        self.createZIP(imagesList, outputFile[: -len(".cbz")] + ".zip")

        # Rename the .zip file to .cbz
        os.rename(outputFile[: -len(".cbz")] + ".zip", outputFile)

    def createZIP(self, imagesList: List[str], outputFile: str) -> None:
        """
        Creates a ZIP file from a list of images.

        CALIBRE HANDLES CBZ BETTER.

        When an image is too wide, first it adds the full image,
        then the smaller divided images.

        Args:
            - imagesList (List[str]): List of image filenames to include in the ZIP.
            - outputFile (str): The path where the output ZIP will be saved.

        Returns:
            - None
        """
        # First we create the folder
        FileHandling.ensureExistance(outputFile[: -len(".zip")])

        width = Counter(
            [Image.open(os.path.join(self.imageFolder, x)).width for x in imagesList]
        ).most_common(1)[0][0]

        # Process images and handle oversized ones
        for image_file in imagesList:

            # Always add the full image
            FileHandling.copyFile(
                self.imageFolder,
                image_file,
                outputFile[: -len(".zip")],
                image_file,
            )

            image_path = os.path.join(self.imageFolder, image_file)
            image = Image.open(image_path)

            # Calculate how many pages this image spans
            pageNumber = round(image.width / width)

            if pageNumber > 1:
                # Image is too wide, divide it into multiple images
                base_filename, extension = os.path.splitext(image_file)

                currentWidth = image.width / pageNumber

                for i in reversed(range(pageNumber)):
                    # Create cropped image for each page
                    left = i * currentWidth
                    right = min((i + 1) * currentWidth, image.width)
                    cropped_image = image.crop((left, 0, right, image.height))

                    # Convert to RGB if necessary
                    if cropped_image.mode == "RGBA":
                        # Create a white background and paste the image on top
                        background = Image.new(
                            "RGB", cropped_image.size, (255, 255, 255)
                        )
                        background.paste(
                            cropped_image, mask=cropped_image.split()[3]
                        )  # Use alpha channel as mask
                        cropped_image = background
                    elif cropped_image.mode != "RGB":
                        cropped_image = cropped_image.convert("RGB")

                    # Save the cropped image to temporal folder
                    # The p is to ensure proper ordering after the whole image
                    divided_filename = (
                        f"{base_filename}p{pageNumber-1-i:03d}{extension}"
                    )
                    divided_path = os.path.join(self.temporalFolder, divided_filename)
                    cropped_image.save(divided_path)

                    # Copy the divided image to the output folder
                    FileHandling.copyFile(
                        self.temporalFolder,
                        divided_filename,
                        outputFile[: -len(".zip")],
                        divided_filename,
                    )

        # Finally we zip the folder
        zipping.zipAndDelete(outputFile[: -len(".zip")])
