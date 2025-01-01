from Modules import Utils
import os


directory = os.path.dirname(os.path.abspath(__file__))

manga = "Berserk"
minimum = "Episode"
division = "Chapter"

naming = {
    "Episode": {"inversion": False, "numeration": False},
    "Title": {"inversion": False, "numeration": True},
    "Volume": {"inversion": False, "numeration": False},
    "Chapter": {"inversion": True, "numeration": False},
    "Arc": {"inversion": True, "numeration": False},
}


Utils.preparationForCBZ(manga, minimum, directory, division, naming)


quit()
