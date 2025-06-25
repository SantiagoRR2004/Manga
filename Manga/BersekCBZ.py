from Modules import mangaUtils
import os


directory = os.path.dirname(os.path.abspath(__file__))

manga = "Berserk"
minimum = "Episode"
division = "Chapter"


mangaUtils.preparationForCBZ(manga, minimum, directory, division)


quit()
