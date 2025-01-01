from Modules import PDFUtils
import os

directory = os.path.dirname(os.path.abspath(__file__))
manga = "Neon Genesis Evangelion"
division = "Stage"

PDFUtils.preparationForPDF(manga, directory, division)
