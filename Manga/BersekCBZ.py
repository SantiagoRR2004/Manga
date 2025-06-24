from Modules import Utils
import os


directory = os.path.dirname(os.path.abspath(__file__))

manga = "Berserk"
minimum = "Episode"
division = "Chapter"


Utils.preparationForCBZ(manga, minimum, directory, division)


quit()
