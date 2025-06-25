from Modules import mangaUtils
import os

directory = os.path.dirname(os.path.abspath(__file__))
manga = "Neon Genesis Evangelion"
division = "Stage"

mangaUtils.preparationForPDF(manga, directory, division)
